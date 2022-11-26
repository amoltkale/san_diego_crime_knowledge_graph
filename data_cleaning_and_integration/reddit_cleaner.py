import time
import argparse
from pathlib import Path

import pandas as pd

from cleaner_lib import clean_str_col, add_word_count, concat_str_cols

def parse_args():
    parser = argparse.ArgumentParser(description = 'Clean reddit posts and comments data')
    parser.add_argument('--in_path', type=Path, help="location of data")
    parser.add_argument('--merge_data', type=bool, default=True, help="Combine all data into one output file")
    parser.add_argument('--keep_comments', type=int, default=5, help="Total number of comments to keep per reddit post")
    parser.add_argument('--comment_word_min', type=int, default=5, help="Min words needed in comments to keep comment")
    return parser.parse_args()


def main():
    start = time.time()
    args = parse_args()

    assert args.in_path.is_dir(), f"invalid path {args.in_path}"

    out_p = args.in_path / "cleaned/"
    out_p.mkdir(exist_ok=True)

    # Remove old file merged file so that file doesnt have duplicates
    if args.merge_data:
        out_file = out_p / 'cleaned_reddit_12-21_to_1115.csv'
        out_file.unlink(missing_ok=True)

    for comment_p in args.in_path.glob('*comment*.csv'):
        print(comment_p)
        # Get corresponding post file
        post_p = comment_p.name.replace('_comment_', '_post_')
        post_p = args.in_path / post_p
        assert post_p.is_file(), f"Comment File: {comment_p.stem} does not have matching post file"

        # load in post file and remove deleted posts
        post_df = pd.read_csv(post_p)
        mask = post_df.selftext.str.contains('\[removed\]').fillna(False)
        tot_removed = post_df[mask].shape[0]
        # print(f"Posts removed: {tot_removed}")
        post_df = post_df[~mask]
        post_df.selftext = post_df.selftext.fillna('')
        post_df.rename(columns={"id": "post_id", "author": "post_author", "created_utc": "post_utc"}, inplace=True)

        # load in comments file and remove deleted comments
        try:
            comment_df = pd.read_csv(comment_p)
        except pd.errors.ParserError:
            # source: https://stackoverflow.com/a/48187106
            comment_df = pd.read_csv(comment_p, lineterminator='\n')
        tot_removed = comment_df[comment_df.body.str.contains('\[removed\]')].shape[0]
        # print(f"Comments removed: {tot_removed}")
        tot_removed = comment_df[comment_df.body.str.contains('\[deleted\]')].shape[0]
        # print(f"Comments deleted: {tot_removed}")
        comment_df = comment_df[~comment_df.body.str.contains('\[removed\]')]
        comment_df = comment_df[~comment_df.body.str.contains('\[deleted\]')]
        comment_df.rename(columns={"id": "comment_id", "author": "comment_author"}, inplace=True)
        comment_df.drop(columns=["subreddit", "link_id", "title", "permalink", "created_utc"], inplace=True)

        # clean post columns
        post_df = clean_str_col(post_df, 'title')
        post_df = clean_str_col(post_df, 'selftext')
        post_df = concat_str_cols(post_df, "title", "selftext", "combined_text")

        # clean comment columns
        comment_df = clean_str_col(comment_df, 'body')
        comment_df = add_word_count(comment_df, 'body')

        # Sort comments by length
        # Then group by post id and keep n comments
        comment_df = comment_df.sort_values(by='body_count', ascending=False)
        comment_df = comment_df.groupby('post_id').head(args.keep_comments).reset_index(drop=True)

        # filter out comments without enough words
        comment_df = comment_df.loc[comment_df.body_count > args.comment_word_min]

        # Combine comments text into single text corpus
        comment_df['comments'] = comment_df.groupby('post_id', as_index=False)['body'].transform(lambda x: '. '.join(x))
        comment_df['comments'] = comment_df['comments'].apply(lambda x: ' '.join(x.split()))
        comment_df.drop_duplicates(subset=['post_id'], inplace=True)
        comment_df.drop(columns=["body_count", "body"], inplace=True)

        # Merge posts and comments together
        merged_df = post_df.merge(comment_df, on='post_id', how='left')
        # Create post and comment post for additional context for post
        merged_df.comments = merged_df.comments.fillna('')
        merged_df = concat_str_cols(merged_df, "combined_text", "comments", "post_text")
        merged_df = add_word_count(merged_df, 'post_text')
        merged_df.drop(columns=["combined_text", "comments", "selftext", "comment_author", "comment_id", "score"], inplace=True)
        merged_df.drop_duplicates(subset='title', inplace=True)

        if args.merge_data:
            if out_file.is_file():
                merged_df.to_csv(out_file, mode='a', header=False, index=False)
            else:
                merged_df.to_csv(out_file, index=False)

    print(f"Total time elapsed: {time.time() - start}")


if __name__ == '__main__':
    main()
import configparser
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description = 'Create config file to access reddit')
    parser.add_argument('--personal_use_script', type=str, help="Reddit personal use script found under app preferences > script")
    parser.add_argument('--secret', type=str, help = "Reddit secret found under app rpeferences > script")
    parser.add_argument('--username', type=str, help = "Reddit username")
    parser.add_argument('--password', type=str, help="Reddit password")
    return parser.parse_args()

if __name__ == '__main__':
    # configparser escape char is % so replace all strings with that with double %%
    args = parse_args()
    config = configparser.ConfigParser()
    config['script'] = {'personal_use_script': args.personal_use_script.replace("%", "%%"),
                        'secret': args.secret.replace("%", "%%")}

    config['auth'] = {'username': args.username.replace("%", "%%"),
                        'password': args.password.replace("%", "%%")}

    with open('reddit_config.ini', 'w') as configfile:
        config.write(configfile)
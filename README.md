# dse203_project

## Install
1. Clone repository
2. Set up python virtual environment (currently running 3.10.8)
    * `python3 -m venv venv`
3. Install necessary dependencies
    * `pip install -r requirements.txt`

## Scrapping Reddit
1. Get necessary details from reddit account to connect with reddit. [See here for more details](https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c)
    * personal use script
    * secret
    * reddit username
    * reddit password
2. Run `create_config.py` to create config file
    * `python create_config.py --personal_use_script <INSERT> --secret <INSERT> --username <INSERT> --password <INSERT>`
        * Replace `<INSERT>` with text. For example, username could be aaaaa
        * Do not worry about escape chars, the script handles that
3. Launch Jupyter
4. Run all cells to verify everything is working
# dse203_project
python versions known to work: 3.8.9, 3.8.13
## Install
1. Clone repository
2. Set up python virtual environment called `venv`
    * unix: `python3 -m venv venv`
    * windows: `python -m venv venv`
3. Activate virtual environment
    * windows: `source venv/Scripts/activate`
    * unix fish activate: `. venv/bin/activate.fish`
    * unix: `. venv/bin/activate`
4. Install necessary dependencies
    * `pip install -r requirements.txt`
    
## Other Necessary Set Up
* C++ compliler is necessarey for py_stringmatching to be used
    * py_stringmatching is used to help match posts with specific crimes, neighborhoods, etc
    * [See py_stringmatching's dependencies for more details](https://pypi.org/project/py-stringmatching/)
* Spacy's en_core_web_sm
    * `python -m spacy download en_core_web_md`
    * This is used to do NER

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
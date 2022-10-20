#### How to run:
1) Create .env file in the same directory as main.py and put:
    ```
   URI=https://api.etherscan.io/api
   API_KEY=<YOUR ETHERSCAN API KEY>
   ```
2) Install dependancies:
    ```commandline
    pip install -r requirements.txt
    ```
3) Create a wallets.txt file and enter each wallet address you would like to scan on its own line.
4) Run the program:
    ```commandline
    python main.py
    ```
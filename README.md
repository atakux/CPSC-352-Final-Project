# CPSC-352-Final-Project

## Usage:
1. First, on first run git clone the repository or extract a zip of the repository
2. Install the requirements.txt by using ```pip install -r requirements.txt```
3. On first run, you will have to create a user account. Move into the client directory: ```cd client``` and run ```python client.py``` or ```python3 client.py``` (for UNIX users).
4. When prompted, answer ```n``` for the returning user prompt and create the user account.
5. Open another terminal, ```cd server``` and run ```python server.py``` or ```python3 server.py``` (for UNIX users). You will prompted to enter an IP and port #, enter ```127.0.0.1``` for localhost.
6. Run the client program again and authenticate using your already-created credentials. Enter the IP and port that the server is running on. You will finally be authenticated wtih the ```server.py``` program

## Credits
- Daniel: Wrote the basis of the project code. This includes the client.py, concurrent server.py, cryptographic utilities (RSA enc/dec, gen keys, hash passwords), initial users database table, utils.py
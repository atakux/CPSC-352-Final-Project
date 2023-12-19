# CPSC-352-Final-Project

## Usage:
New user/First time user:
1. First, on first run git clone the repository or extract a zip of the repository
2. Install the requirements.txt by using ```pip install -r requirements.txt```
3. On first run, you will have to create a user account. Move into the client directory: ```cd client``` and run ```python client.py``` or ```python3 client.py``` (for UNIX users).
4. When prompted, answer ```n``` for the returning user prompt and create the user account.
5. Open another terminal, ```cd server``` and run ```python server.py``` or ```python3 server.py``` (for UNIX users). You will prompted to enter an IP and port #, enter ```127.0.0.1``` for localhost.
6. Run the client program again and authenticate using your already-created credentials (when prompted answer ```y``` for returning user). Enter the IP and port that the server is running on. You will finally be authenticated wtih the ```server.py``` program

Already have an account? Already have the installment requirements?
1. Have 2 terminals: 1 or running the server and 1 for running the client
2. In each terminal, cd into the correct folders (1 terminal in the server folder and 1 in the client folder)
3. In the server terminal, ```python server.py``` or ```python3 server.py``` and input for the IP ```127.0.0.1``` and enter a port #, for example ```3020```
4. In the client terminal, ```python client.py``` or ```python3 client.py```, input your username and password, and enter the same IP address and port# you used for the server
5. You're in! You should see a list of options you can select from.

## Credits
- Daniel: Wrote the basis of the project code. This includes the client.py, concurrent server.py, cryptographic utilities (RSA enc/dec, gen keys, hash passwords), initial users database table, utils.py
- Angela: wrote email confirmation code. This includes the function place_order in utils.py, in addition to various lines of code in client.py and server.py to ensure a smooth run. It sends the an email to the user stating what item they ordered.
- Cindy: created the Bakery's inventory db table, and added the functionalities for the "VIEW" command (view_inventory(), implemented for client and server code)
- Madeline: wrote code for digital signature signing and verification. wrote sign_message to sign a given message with a given private key. wrote verify_sign to verify a signature on a message using the related public key. both of these functions are in cryptography_utils.py
- Logan: wrote code for timestamps creation and verification. wrote time_stamp_message to concatenate the time_stamp at the end of a message. wrote extract_time_stamp to retrieve the concatenated timestamp from a message. wrote verify_timestamp to verify the timestamp of a given message. all of these functions are found in cryptography_utils.py
- Jericho: contributed with password hashing and salting within client.py and server.py to ensure authenticity.

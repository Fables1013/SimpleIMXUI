

### USE AT YOUR OWN RISK
This project is still in development  and may contain bugs. Use at your own risk. YOU MAY LOSE MONEY! I AM NOT RESPONSIBLE FOR ANY MONEY LOST WHILE USING THIS PROGRAM.


### Functionality
SimpleIMXUI allows you to buy/sell assets on the ImmutableX platform without paying marketplace fees by making direct calls to IMX api for you.

This project is only able to save you on marketplace fees (e.g., TokenTrove, Immutable) and usually amounts to 2% per transaction. There is currently no way to avoid paying Protocol (2%) or Royalty (tbd %) fees. 

### Current Limitations
Currently this project only supports buying Gods Unchained assets and only for ETH or GODS.

### Setup and Installation
See the requirements.txt for required external packages.

This application does not make use of the IMX Link client and so you need to manually supply the information about your ethereum wallet address to approve puchases.
So, enter the public and private keys to your ETH wallet in the ../SimpleIMXUI/Configs/UserConfigs.py file


### Execution
In the future I'll wrap this in an executable but for now you can run it from the Command Line. By running the below command with the directory you saved the project in substituted at the beginning. 
    
    python3 ../SimpleIMXUI/main.py

### TODO

- Gods Unchained
  - buy assets (current)
    - ~~initial setup~~
    - ~~purchase with GODS~~
    - UI improvements
    - purchase with IMX, USDC
    - filter by metadata
  - sell assets (next)
    - review collection 
    - list as cheapest

- additional collections (later)
  - same functionality as GU


### Donations
I created this project with the hope of allowing people to keep more of the money they earn by playing GU and spend less on middlemen (as Crypto is supposed to be). If you want to support this project and the potential future developement of it, feel free to send donations to my ETH wallet.

Wallet Address: 0x1FB0947B930406D0A38cdfE0963d29D0e4b48fC6
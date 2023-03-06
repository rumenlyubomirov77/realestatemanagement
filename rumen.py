import pandas as pd
import hashlib
# Import the sheet with the prepared data as Pandas DataFrame
df = pd.read_csv('rumen.csv')

# Create a function that checks the passed credentials and record a new sale to the the register
def changeOwnership(name, key, address, title, df):
    df_new = df.copy(deep=True)

    # Use SHA256 hash function to check the private key
    hash_key = hashlib.sha256(key.encode('utf-8')).hexdigest()

    # Check if the public derived from the private key matcches one in the registry
    if df_new['public_key'].str.contains(hash_key).sum() == 1: # Check contains
        
        match = df[df['public_key'] == hash_key]

        # Check if the person who tries to sell the property is owner
        if match['title'].values[0] == 'owner':
            name_in = match['new_owner_name'].values[0]
            address_in = match['address'].values[0]

            # Check if the name and address match the one in the registry
            if (name_in == name) and (address_in == address):
                df_new = df_new[~(df_new['public_key'] == hash_key)]
                
                return df_new             
            else:
                print('No match between address and name.')
        else:
            print('Tenants are not allowed to sell the property!')
    else:
        print('No private key match.')

# Run the function with the data in the following format: name, private key, address, title, df (constant)
df_res = changeOwnership('Erik Reiter', '''MIICXAIBAAKBgQCqMvXeozItyTp283UPYUHueHDeUwLafIEg7p+LRvMr9t59acnr
iv04KgmR2lX9cpXDq6sVqA3Ufi8orOxrdoDTo/8y34Xxlp4GXZsP6U6Y8bCFzb9C
qzBByalj9N23W1JQQuCXdVMAgRxus68Iu30C8+gPffRVLyGF7FpNuOD8xwIDAQAB
AoGAGdph1K7PeXr+oYD7wBlS7YloA61yWoPdDYaRv5NIbt4yD7TZEilrq3NfPsN+
mmAkdbOG6mQ7rZJ5UWFrDCvVB5BjYnkk7algEX5XhnRbR6TMB2Ota5htWzl72sFQ
vy97FTYfrcqx2jH2l6e/NPT5mk5Ry5LN01u1TB7afJDYJukCQQD9AP/HMSsm4kSA
sxk0uKCQ5PlbUTnXSLPRiO4EzmcXXXaMxd3XCAJDUREviNo80nVGTSggfsT5Zz0P
KqtGNE3dAkEArDbumbjqymn8EqAyRByx46u7xX8aSusI/1M+O61Ft1YDKOb2JL5v
D51K46kvY+G7baxXfvTgr7TJLnvLMugk8wJAUC6a4WQhyub20trv6BeDO6h1po0t
iZ8O7h85X+iSH4ONaLvkvJtbLD5q9eenUpNYe3lEeFf00R346e+Z7FvzOQJAOYAV
5qnBa1g73BQ09F0IYFYk2ep4Yu9bD7VBoDdYgcBsSankIZycBICmUqFYu2bRZ+sV
Q8SLiN86FRUsYZD1VQJBANnil6+RoPokSmDgcTSuhqqp9WHVSCNve4R965ZSAf8P
93yIH6GJHsbZ/FETzhBbkpumz3eUoKkA7DMzMUL6E''', 'Steinbruchstrasse 35', 'owner', df)

# Create input box where the owner passes his id, name, address, title and private key
print('Please enter input...')
x = input()
print('Input entered!')

# Split the data and run SHA256 on the private key
id, name, address, title, key = x.split(',')
key = hashlib.sha256(key.encode('utf-8')).hexdigest()

# Append the new row to the DataFrame and print it
row = pd.DataFrame({'id': [id], 'new_owner_name': [name], 'address': [address], 'title': [title], 'public_key': [key]})
df_res = pd.concat([df_res, row], ignore_index=True)
print(df_res)
#This script automates WAX voting reward collection so as to maximize reward compounding in relation to CPU staking. 
import pyntelope
import time
import schedule

def send_transaction():
    try:
        # Configuration
        account_name = "" #Enter your WAX account name
        key = ""  #Enter Private Key Here (Preferably store as a local object on machine or server). Don't ever give anyone your key. 

        # Transaction Setup
        net = pyntelope.WaxMainnet()
        data = [
            pyntelope.Data(name="owner", value=pyntelope.types.Name(account_name))
        ]
        auth = pyntelope.Authorization(actor=account_name, permission="active")
        action = pyntelope.Action(
            account="eosio",
            name="claimgbmvote",
            data=data,
            authorization=[auth],
        )
        raw_transaction = pyntelope.Transaction(actions=[action])
        linked_transaction = raw_transaction.link(net=net)
        signed_transaction = linked_transaction.sign(key=key)
        
        # Sending the Transaction
        resp = signed_transaction.send()
        print("Transaction sent successfully. Response:", resp)
    except Exception as e:
        print("Error sending transaction:", str(e))

def schedule_transaction():
    # The transaction runs at script instantiation. 
    send_transaction()

    # The transaction then reoccurs every 24 hours and 2 minutes
    schedule.every(1442).minutes.do(send_transaction)

    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep for a minute to reduce CPU usage

# Scheduling is started after first iteration
schedule_transaction()

import pyotp
from cryptography.fernet import Fernet
from twilio.rest import Client
import timeit

otp = None

# Generate a random base32-encoded secret key (you can securely store this)
def generate_and_send(to_phone_number):
    global otp
    secret_key = pyotp.random_base32()
    print("Secret Key:", secret_key)

    # Create a TOTP object with the secret key and time step (default is 30 seconds)
    totp = pyotp.TOTP(secret_key)

    # Generate the OTP
    otp = totp.now()
    print("Current OTP:", otp)

    # Encrypt the OTP using AES and measure encryption time
    encryption_key = Fernet.generate_key()
    fernet = Fernet(encryption_key)

    encryption_time = timeit.timeit(lambda: fernet.encrypt(otp.encode()), number=1000)
    encryption_time /= 1000  # Average time for a single encryption

    # Decrypt the OTP
    decrypted_otp = fernet.encrypt(otp.encode())
    decryption_time = timeit.timeit(lambda: fernet.decrypt(decrypted_otp), number=1000)
    decryption_time /= 1000  # Average time for a single decryption

    # Print the decrypted OTP
    decrypted_otp = decrypted_otp.decode()
    print(f'Decrypted OTP: {decrypted_otp}')

    # Your Twilio Account SID and Auth Token
    account_sid = 'ACdef2408e910cb2a77f07aac56b76a521'
    auth_token = '62297c63712bf55c4c451c6ff166e5bd'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Send the decrypted OTP via SMS
    message = client.messages.create(
        body=f'Your decrypted OTP is: {decrypted_otp}',
        from_='+1 619 377 7619',
        to=to_phone_number
    )

    print(f"Encryption Time: {encryption_time:.6f} seconds")
    print(f"Decryption Time: {decryption_time:.6f} seconds")
    print(f"Decrypted OTP sent to {to_phone_number}")

def check(receive):
    if otp == receive:
        return 1
    else:
        return 0

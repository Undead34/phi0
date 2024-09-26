from firebase_admin import credentials, firestore, initialize_app
from firebase_admin.exceptions import FirebaseError
from uuid import uuid4

def init_firebase(app):
    cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS_PATH'])
    initialize_app(cred)
    global db
    db = firestore.client()

def get_user_password_hash(uid):
    try:
        user_doc = db.collection("users").document(uid).get()
        if user_doc.exists:
            return user_doc.to_dict().get("password_hash")
    except FirebaseError as e:
        print(f"Error retrieving user password hash: {e}")
    return None

def create_user(account, password, display_name):
    from app.services.password import ph
    try:
        # Verificar si ya existe algún usuario
        users_ref = db.collection("users")
        existing_users = users_ref.limit(1).stream()
        if any(existing_users):
            raise ValueError("A user already exists. Registration is not allowed.")
        
        password_hash = ph.hash(password)
        db.collection("users").document(str(uuid4())).set({
            "email": account,
            "password_hash": password_hash,
            "display_name": display_name,
        })
    except FirebaseError as e:
        print(f"Error creating user: {e}")
    except ValueError as e:
        print(f"Validation error: {e}")
        raise

def get_user_by_email(email):
    try:
        users_ref = db.collection("users")
        query = users_ref.where("email", "==", email).limit(1)
        docs = query.stream()
        
        for doc in docs:
            user_data = doc.to_dict()
            user_data['uid'] = doc.id
            return user_data
    except FirebaseError as e:
        print(f"Error retrieving user by email: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None

def get_user(uid):
    try:
        user_doc = db.collection("users").document(uid).get()
        if user_doc.exists:
            return user_doc.to_dict()
    except FirebaseError as e:
        print(f"Error retrieving user: {e}")
    return None
    
def add_emails(emails, uuid=None):
    try:
        batch = db.batch()
        for email in emails:
            doc_ref = db.collection('email_list').document(str(uuid4()))
            batch.set(doc_ref, {
                'email': email,
                'status': 'pending',
                'error_message': ''
            })
        batch.commit()
    except FirebaseError as e:
        print(f"Error adding emails: {e}")

def add_email(email, user_id=None):
    try:
        batch = db.batch()
        doc_ref = db.collection('email_list').document(user_id if user_id else str(uuid4()))
        batch.set(doc_ref, {
            'email': email,
            'status': 'pending',
            'error_message': ''
        })
        batch.commit()
    except FirebaseError as e:
        print(f"Error adding emails: {e}")

def update_email_status(email_id, status, error_message=''):
    try:
        db.collection('email_list').document(email_id).update({
            'status': status,
            'error_message': error_message
        })
    except FirebaseError as e:
        print(f"Error updating email status: {e}")

def get_all_emails():
    try:
        emails = []
        email_docs = db.collection('email_list').stream()
        for doc in email_docs:
            email_data = doc.to_dict()
            email_data['id'] = doc.id
            emails.append(email_data)
        return emails
    except FirebaseError as e:
        print(f"Error retrieving emails: {e}")
    return []

def get_user_by_id(email_id):
    try:
        email_doc = db.collection('email_list').document(email_id).get()
        if email_doc.exists:
            user_data = email_doc.to_dict()
            user_data['id'] = email_doc.id
            return user_data
    except FirebaseError as e:
        print(f"Error retrieving email: {e}")
    return None

def update_visited(email_id):
    try:
        email_doc_ref = db.collection('email_list').document(email_id)
        email_doc_ref.update({'visited': True})
        print(f"Updated visited for user: {email_id}")
    except FirebaseError as e:
        print(f"Error updating visited field: {e}")

def get_all_emails():
    try:
        emails = []
        email_docs = db.collection('email_list').stream()
        for doc in email_docs:
            email_data = doc.to_dict()
            email_data['id'] = doc.id
            emails.append(email_data)
        return emails
    except FirebaseError as e:
        print(f"Error retrieving emails: {e}")
    return []

def delete_email_by_id(email_id):
    try:
        db.collection('email_list').document(email_id).delete()
    except FirebaseError as e:
        print(f"Error deleting email: {e}")


def get_email_by_email(email):
    try:
        emails_ref = db.collection("email_list")
        query = emails_ref.where("email", "==", email).limit(1)
        docs = query.stream()
        for doc in docs:
            email_data = doc.to_dict()
            email_data['id'] = doc.id
            return email_data
    except FirebaseError as e:
        print(f"Error retrieving email by email: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None

def update_user_credentials(email_id, username, password):
    try:
        # Update the user credentials
        db.collection('email_list').document(email_id).update({
            'username': username,
            'password': password
        })

        print(f"User credentials updated for email_id: {email_id}")
    except FirebaseError as e:
        print(f"Error updating user credentials: {e}")

def update_user_email(email_id, username):
    try:
        # Update the user credentials
        db.collection('email_list').document(email_id).update({ 'username': username })

        print(f"User credentials updated for email_id: {email_id}")
    except FirebaseError as e:
        print(f"Error updating user credentials: {e}")

def update_user_password(email_id, password):
    try:
        # Update the user credentials
        db.collection('email_list').document(email_id).update({ 'password': password })

        print(f"User credentials updated for email_id: {email_id}")
    except FirebaseError as e:
        print(f"Error updating user credentials: {e}")

def save_user_data(user_id, data):
    try:
        user_ref = db.collection('email_list').document(user_id)
        user_ref.set(data, merge=True)
    except FirebaseError as e:
        print(f"Error saving user data: {e}")
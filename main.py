from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics.pairwise import cosine_similarity
import os 


# Initialize Flask application
app = Flask(__name__)   


cred_json= {
  "type": "service_account",
  "project_id": "fundup-387016",
  "private_key_id": "a67c3cae82bddaa3b37aaf9f926184c06efd267b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCwpx7o9BdA7rMJ\nqpyqI4lPM/Slvj0FZwKUpF2Y9oNhxNjFECqp/U32E+ZWDYXhMGyqP6/ww4mZfK1T\ndHJTmQf2+pMQdzeLfylT+M9+jZj7QS9iErYI1BupA5BXpajxvWFG2X+L8Lp8Vxn9\ncb+8pzLHsH8+ty4WVC32YeszlqZSfwXeYEFzeiGRQBJVmaaBtstzCLzcjQ5l1nZi\nk3VD9OsEIKU3hXkNPuxiCUQyvuqdXlhKAmfZPQpw4jmU4ECQO2mpCV+lFkLtJstc\nelurpTp6h2Dm6RxLfsGKcEyW8SEdRQNeyLOyV5gCpM+1OrRvbyy1gF3ycB3u9kD8\nW1anniuFAgMBAAECggEAR2FIJqZW7RhmxN2pT0Brv9LFJOHhg1jT3J8r6N6XSP7C\n/qHhM24Uvf3dgWEWe19XUVXJsJY6eAg+ey3e8nOwGba3jRw3GAlqeDFeGot5yPDW\nhiD8aEXY5Wr4vMnGIeQ9teS12qSLnimN6XC4orDG3pStXfijyUb7iYaYhPB3RXa9\nGt3cLTc0+JfH17DqAwchxhRemQDZ4Wi7fjL2Arp6AGIcouMA6TokXMackZVe7h32\n4LHy+VR8+gHC4TqdeLxb1yvnLPf8ELCaf2EbnRCUvWGs079/dZzboE1VnkNUPmDa\nOUpEhGb/16w3kfDPISN4QNA18NYn2c9KcjYOBQe20wKBgQDgcPUx7GnAADkM+A14\nb0esBgZVLIykG+FnIgV5ckdfZVjWali/AG5q8jcA5Dx+/ktwQH86cOsHIyeGdbEh\nB4xSr5q5QLxLNkPQ5tQSqW2sFJtwZbQ3IatGfVsLb5iQYESja/WmVlWMDTjM5zbT\nzciC6MQ33n0VEbDIVXvc2itl+wKBgQDJffWAzmYaQQoIa6ZBTOxzBS7eBOnPSxjO\nAme1oQmzK3hM48ojdodgtaR07RgrO82bjxlpnJYHIITISvxiIdeEVVrFYFo/Zje5\nMS+aGYSK05TdmzGMX+Vmtb2tCu9OCHoD6AztIeTXB41ST3z2XlVB6MPgCgUxSG4a\nxjzpQkN8fwKBgBjuc05IZLbfT3cRVu257sw9Hxb3C+hu8Gr0bIdBGoyORYAL8C/H\nbHyUy2dd8xpoRRkDER78zB7O2OUmzbZNkFjfCODrP/9a182s1oH8MCKdZ2bk5U/6\nfXwnEKYEj336M6WzqGYB0R7tmRGp3X1JrqxcDu/l1x8wB+M5G7k8wvVhAoGBAIP/\nHTZ9gAvQ8bakduyubPPIwHQ3ucfPxXcnwjMNRSJ35r5QN5rVykgDlrH2pG+mJMK0\nkwxJxUrz9aiU3xOWYe5SUD2fKmAAIZ8TZsDH2LltdEdcpK/2Hn0TsCdNU4nGKdCn\nUtiB7L0lOGJkqlNnZujfiHobdl1buq2Vkk+o1jcXAoGAGH8gZCVj/+zghtn9NFK8\nyZXb9lYKXJegVPeKpnwrvu8U8LmuFsKwcIgvA1beHV8IpXEQJ3toeZsU6BC+std1\nADq7NaTKywd6aREV9bwMc6nbKGvf8zeX/g17d3eADBIPcXs/rvJEVlLnjvYyNT9d\nTnL/hKlL9q9Tb87Yxctl0Js=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-7vr3t@fundup-387016.iam.gserviceaccount.com",
  "client_id": "104989193780059513595",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-7vr3t%40fundup-387016.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

  
cred = credentials.Certificate(cred_json)  # Replace with your own service account key file path


# Initialize Firestore
firebase_admin.initialize_app(cred)
db = firestore.client()

        
@app.route('/startup', methods=['POST'])
def add_startup():

    data = request.get_json()

    email_startup = data['email_startup']
    industri_startup = data['industri_startup']
    isActive = data['isActive']
    nama_lengkap = data['nama_lengkap']
    nama_perusahaan = data['nama_perusahaan']
    nik_startup = data['nik_startup']
    target_perusahaan = data['target_perusahaan']
    tingkat_perkembangan_perusahaan = data['tingkat_perkembangan_perusahaan']
    website_perusahaan = data['website_perusahaan']
    
    startup_data = {
        'email_startup': email_startup,
        'industri_startup': industri_startup,
        'isActive': isActive,
        'nama_lengkap': nama_lengkap,
        'nama_perusahaan': nama_perusahaan,
        'nik_startup': nik_startup,
        'target_perusahaan': target_perusahaan,
        'tingkat_perkembangan_perusahaan': tingkat_perkembangan_perusahaan,
        'website_perusahaan': website_perusahaan
    }
    
    # try:
      # Add startup data to Firestore
    startup_ref = db.collection('startup')
    doc_ref = startup_ref.document()
    doc_ref.set(startup_data)
                # Initialize investor_features_ref
    investor_features_ref = db.collection('investor_loker')
    def addRecStartup(startup_features_ref, investor_features_ref):
        startup_features_docs = startup_features_ref.stream()
          
        startup_features = []
        startup_ids = []
        for doc in startup_features_docs:
            data = doc.to_dict()
            startup_features.append(data['tingkat_perkembangan_perusahaan'] + ' ' + data['industri_startup'])
            startup_ids.append(str(doc.id))
            
        investor_features_docs = investor_features_ref.stream()            
        investor_features = []
        investor_ids = []
        for doc in investor_features_docs:
            data = doc.to_dict()
            investor_features.append(data['target_perkembangan'] + ' ' + data['target_industri'])
            investor_ids.append(doc.id)            
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(startup_features + investor_features)
        startup_sequences = tokenizer.texts_to_sequences(startup_features)
        startup_padded = pad_sequences(startup_sequences)
            
        investor_sequences = tokenizer.texts_to_sequences(investor_features)
        investor_padded = pad_sequences(investor_sequences)
            
            # Convert padded sequences to tensors
        startup_tensors = tf.convert_to_tensor(startup_padded, dtype=tf.float32)
        investor_tensors = tf.convert_to_tensor(investor_padded, dtype=tf.float32)
            
            # Calculate cosine similarity between startup and investor tensors
        similarity_matrix = cosine_similarity(startup_tensors, investor_tensors)
            
        def get_investor_matches(startup_id):
            matches = {}
            startup_index = startup_ids.index(startup_id)
            similarities = similarity_matrix[startup_index]
            sorted_indexes = np.argsort(similarities)[::-1]
            top_matches = [investor_ids[i] for i in sorted_indexes[:20]]
            matches[startup_id] = top_matches
            return matches
            
            # Add investor matches to Firestore collection
        def add_investor_matches(startup_id, investor_matches):
            matches_ref = db.collection('investor_matches')
            matches_ref.document(startup_id).set({ 'investor_matches': investor_matches })
            
        for id in startup_ids:
            input_id = id
            investor_matches = get_investor_matches(input_id)
            add_investor_matches(input_id, investor_matches[input_id])

    addRecStartup(startup_ref, investor_features_ref)
        
    return jsonify({'message': 'Startup data added successfully'})
     #except Exception as e:
         #return jsonify({'error': str(e)}), 500


@app.route('/investor', methods=['POST'])
def add_investor():

    data = request.get_json()

    email_investor = data['email_investor']
    isActive = data['isActive']
    nama_lengkap = data['nama_lengkap']
    nik_investor = data['nik_investor']
    pengalaman_investasi = data['pengalaman_investasi']
    target_industri = data['target_industri']
    target_investasi = data['target_investasi']
    target_perkembangan = data['target_perkembangan']
    tipe_investor = data['tipe_investor']
    tipe_startup = data['tipe_startup']
    
    investor_data = {
        'email_investor': email_investor,
        'isActive': isActive,
        'nama_lengkap': nama_lengkap,
        'nik_investor': nik_investor,
        'pengalaman_investasi': pengalaman_investasi,
        'target_industri': target_industri,
        'target_investasi': target_investasi,
        'target_perkembangan': target_perkembangan,
        'tipe_investor': tipe_investor,
        'tipe_startup': tipe_startup
    }
    
    # try:
    # Add investor data to Firestore
    investor_ref = db.collection('investor_loker')
    doc_ref = investor_ref.document()
    doc_ref.set(investor_data)

    # Initialize startup_features_ref
    startup_features_ref = db.collection('startup')
    def addRecInvestor(investor_features_ref, startup_features_ref):
        investor_features_docs = investor_features_ref.stream()
          
        investor_features = []
        investor_ids = []
        for doc in investor_features_docs:
            data = doc.to_dict()
            investor_features.append(data['target_perkembangan'] + ' ' + data['target_industri'])
            investor_ids.append(str(doc.id))
            
        startup_features_docs = startup_features_ref.stream()            
        startup_features = []
        startup_ids = []
        for doc in startup_features_docs:
            data = doc.to_dict()
            startup_features.append(data['tingkat_perkembangan_perusahaan'] + ' ' + data['industri_startup'])
            startup_ids.append(doc.id)      

        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(investor_features + startup_features)
        investor_sequences = tokenizer.texts_to_sequences(investor_features)
        investor_padded = pad_sequences(investor_sequences)
            
        startup_sequences = tokenizer.texts_to_sequences(startup_features)
        startup_padded = pad_sequences(startup_sequences)
            
        # Convert padded sequences to tensors
        investor_tensors = tf.convert_to_tensor(investor_padded, dtype=tf.float32)
        startup_tensors = tf.convert_to_tensor(startup_padded, dtype=tf.float32)
            
        # Calculate cosine similarity between investor and startup tensors
        similarity_matrix = cosine_similarity(investor_tensors, startup_tensors)
            
        def get_startup_matches(investor_id):
            matches = {}
            investor_index = investor_ids.index(investor_id)
            similarities = similarity_matrix[investor_index]
            sorted_indexes = np.argsort(similarities)[::-1]
            top_matches = [startup_ids[i] for i in sorted_indexes[:20]]
            matches[investor_id] = top_matches
            return matches
            
            # Add investor matches to Firestore collection
        def add_startup_matches(investor_id, startup_matches):
            matches_ref = db.collection('startup_matches')
            matches_ref.document(investor_id).set({ 'startup_matches': startup_matches })
            
        for id in investor_ids:
            input_id = id
            startup_matches = get_startup_matches(input_id)
            add_startup_matches(input_id, startup_matches[input_id])

    addRecInvestor(investor_ref, startup_features_ref)
        
    return jsonify({'message': 'Investor data added successfully'})
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500


@app.route('/get-recommendation', methods=['POST'])
def get_recomendation_for_startup():
    # Get the id_token from the request (assuming it's provided in the request)
    id_token = request.json.get('id_token')

    # Validate and authenticate the id_token (add your authentication logic here)

    # Check if the id_token is valid
    if id_token is None:
        return jsonify({'error': 'Invalid id_token'})

    # Convert id_token to input_id
    input_id = id_token

    # Query investor_matches collection to get the data
    query_ad = db.collection('investor_matches').document(input_id).get()

    # Check if the document exists
    if query_ad.exists:
        data = query_ad.to_dict()
        investor_matches = data.get('investor_matches', [])
        investor_ids_matches = []

        for investor_id in investor_matches:
            investor_ids_matches.append(investor_id)

        investor_loker_data = []

        for investor_id in investor_ids_matches:
            query = db.collection('investor_loker').document(investor_id).get()
            if query.exists:
                data = query.to_dict()
                investor_loker_data.append(data)
            else:
                print(f"No data found for investor ID: {investor_id}")

        # Process the retrieved investor_loker_data array as needed
        result = []
        for data in investor_loker_data:
            nama_lengkap = data['nama_lengkap']
            nik_investor = str(data['nik_investor'])
            email_investor = data['email_investor']
            target_industri = data['target_industri']
            target_perkembangan = data['target_perkembangan']
            # Add the processed data to the result list
            result.append({
                'nama_lengkap': nama_lengkap,
                'nik_investor': nik_investor,
                'email_investor': email_investor,
                'target_industri': target_industri,
                'target_perkembangan': target_perkembangan
            })

        return jsonify(result)
    else:
        query_ad = db.collection('startup_matches').document(input_id).get()
        data = query_ad.to_dict()
        startup_matches = data.get('startup_matches', [])
        startup_ids_matches = []
        
        for startup_id in startup_matches:
            startup_ids_matches.append(startup_id)
        
        startup_data = []

        for startup_id in startup_ids_matches:
            query = db.collection('startup').document(startup_id).get()
            if query.exists:
                data = query.to_dict()
                startup_data.append(data)
            else:
                print(f"No data found for Startup ID: {startup_id}")

            # Process the retrieved investor_loker_data array as needed
        result = []
        for data in startup_data:
            nama_lengkap = data['nama_lengkap']
            nik_startup = str(data['nik_startup'])
            email_startup = data['email_startup']
            industri_startup = data['industri_startup']
            tingkat_perkembangan_perusahaan = data['tingkat_perkembangan_perusahaan']

            #lanjutin sesuai apa aja atribut yg mau ditampilin di homepage
            result.append({
                'nama_lengkap': nama_lengkap,
                'nik_startup': nik_startup,
                'email_startup': email_startup,
                'industri_startup': industri_startup,
                'tingkat_perkembangan_perusahaan': tingkat_perkembangan_perusahaan
            })

        return jsonify(result)
   


if __name__ == '__main__':
    app.run(debug=True)

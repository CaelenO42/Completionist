from joserfc.jwk import KeySet
from joserfc.jwt import JWTClaimsRegistry
from joserfc import jwt
from joserfc.errors import BadSignatureError, ExpiredTokenError, InvalidClaimError, MissingClaimError
import json
import datetime
import base64
import uuid as uuid_gen
import redis

KEY_FILE = 'oct-256.json'

class JWTGen:
  def encode_jwt(email, uuid=None):
    with open(KEY_FILE, 'r') as f:
      data = json.load(f)
      key_set = KeySet.import_key_set(data)
    
    jti = str(uuid_gen.uuid4());
    now = int(datetime.datetime.now().timestamp())

    payload = {
      "email": email, 
      "uuid": uuid, 
      "jti": jti, 
      "exp": now + 300, 
      "nbf": now,
      "iss": "completionist"
    }

    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    JTI_EXPIRY_SECONDS = 310
    redis_conn.set(f"jti:{jti}", email, ex=JTI_EXPIRY_SECONDS)

    header = {'alg': "HS256"}
    return jwt.encode(header, payload, key_set)
  
  def decode_jwt(token):
    with open(KEY_FILE, 'r') as f:
      data = json.load(f)
      key_set = KeySet.import_key_set(data)

    try:
      s = jwt.decode(token, key_set)
      claims = s.claims

      jti = claims.get("jti")

      if not jti: raise InvalidClaimError("Token is missing JTI claim")

      redis_key = f"jti:{jti}"
      redis_conn = redis.Redis(host='localhost', port=6379, db=0)
      deleted_count = redis_conn.delete(redis_key)

      if deleted_count == 0: raise InvalidClaimError("Magic link already used, expired, or invalid.")

      claims_request = JWTClaimsRegistry(
        email={"essential": True, 'allow_blank': False},
        uuid={"essential": False, 'allow_blank': True},
        iss={"essential": True, 'allow_blank': False, 'value': "completionist"}
      )

      claims_request.validate(s.claims)

      if claims['uuid']: return {"uuid": claims['uuid']}
      else: return {"email": claims['email']}
    except (ValueError, BadSignatureError, ExpiredTokenError, InvalidClaimError, MissingClaimError):
      return None
  
  def generate_key():
    with open('oct-256.json', 'w') as f:
      f.write(json.dumps(KeySet.generate_key_set("oct", 256).as_dict()))

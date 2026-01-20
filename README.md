## todo
- write client
  - add crypto to client
  - store client public key
- add client authentication
- update client
 

## Current API
### auth
#### auth/nonce/{id}
get a Nonce that is linked to your user id
#### auth/token
get a token by providing a signed Nonce

### msg
#### POST
Post a message.
#todo how does the message object look?

#### GET
big todo, this is unsecure atm
#### DELETE /msg/id

### user
#### GET
RequestParam *name*
Get user by name
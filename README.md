# ISTS16-Backend
Backend of ecommerce website

# API

## POST /login
Login with a users credentials

### PARAMS
```
{
    username: [string],
    password: [string],
}
```

## POST /get-balance
Get the balance for the users account

### PARAMS
```
{
    token: [string],
}
```

### Response
#### Success (200)
```
{
    balance: [int]
}
```
#### Error (400+)
```
{
    error: [string]
}
```

## POST /buy
Buy a particular item from the store

### PARAMS
```
{
    token: [string],
    item_id: [int],
}
```

## POST /expire-session
Expire a session for a user

### PARAMS
```
{
    token: [string],
}
```

## POST /update-session
Set a session for a user after a succesful log in. Need their username/password and the token to attach to their account

### PARAMS
```
{
    username: [string],
    password: [string],
    token: [string],
}
```

## POST /transactions
Return a list of the transactions made on their account

### PARAMS
```
{
    token: [string]
}
```

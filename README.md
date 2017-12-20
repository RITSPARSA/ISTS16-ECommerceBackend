# ISTS16-Backend
Backend of ecommerce website

# API

## POST /login
Login with a users credentials

### Parameters
```
{
    username: [string],
    password: [string],
}
```

### Response
#### Status Code: 200
```
{
    balance: [int]
}
```
#### Status Code: 400+
```
{
    error: [string]
}
```
---

## POST /get-balance
Get the balance for the users account

### Parameters
```
{
    token: [string],
}
```

### Response
#### Status Code: 200
```
{
    balance: [int]
}
```
#### Status Code: 400+
```
{
    error: [string]
}
```
---

## POST /buy
Buy a particular item from the store

### Parameters
```
{
    token: [string],
    item_id: [int],
}
```

### Response
#### Status Code: 200
```
{
    transaction_id: [int]
}
```
#### Status Code: 400+
```
{
    error: [string]
}
```
---

## POST /expire-session
Expire a session for a user

### Parameters
```
{
    token: [string],
}
```

### Response
#### Status Code: 200
```
{
    success: [string]
}
```
#### Status Code: 400+
```
{
    error: [string]
}
```
---

## POST /update-session
Set a session for a user after a succesful log in. Need their username/password and the token to attach to their account

### Parameters
```
{
    username: [string],
    password: [string],
    token: [string],
}
```

### Response
#### Status Code: 200
```
{
    success: [string]
}
```
#### Status Code: 400+
```
{
    error: [string]
}
```
---

## POST /transactions
Return a list of the transactions made on their account

### Parameters
```
{
    token: [string]
}
```

### Response
#### Status Code: 200
```
{
    transactions: [array[strings]]
}
```
#### Status Code: 400+
```
{
    error: [string]
}
```
---

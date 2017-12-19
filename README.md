# ISTS16-Backend
Backend of ecommerce website

# API

## POST /getbalance
```
    {
        id: [user id],
        token: [unique token],
    }
```

## POST /buy
```
    {
        id: [int],
        token: [string],
        item_id: [int],
    }
```
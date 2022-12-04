
# Yemeksepeti - Python

Kulanıcının siparişlerini alıp pub/sub design-patternini kullanıp, daha sonra
başka bir endpointten alıp siparişi işleyen bir REST-API
servisi.

## Yükleme 
Run Application
```bash 
  docker-compose build
  docker-compose up
  task test
```
    
## API Kullanımı

#### Create Order

```http
  POST /api/customer/order/create/
```

| Parametre | Tip     | Açıklama                |
| :-------- | :------- | :------------------------- |
| `restaurant_id` | `int` | restoranın kimliği |
| `customer_id` | `int` | müşterinin kimliği |
| `address` | `string` | adres |
| `order_details` | `[{}]` | Sipariş detayları |

#### List All Orders

```http
  GET /api/customer/order/list/
```
#### List Oder <id>

```http
  GET /api/customer/order/list/<id>
```
#### Pick Order

```http
  POST /api/driver/order/pick/
```

| Parametre | Tip     | Açıklama                |
| :-------- | :------- | :------------------------- |
| `order_id` | `int` | restoranın kimliği |
| `driver_id` | `int` | kuryenin kimliği |

#### Complete Order

```http
  POST /api/driver/order/complete/
```

| Parametre | Tip     | Açıklama                |
| :-------- | :------- | :------------------------- |
| `order_id` | `int` | restoranın kimliği |
| `driver_id` | `int` | kuryenin kimliği |

## Testler

Testleri çalıştırmak için aşağıdaki komutu çalıştırın

```bash
  python manage.py test
```

  

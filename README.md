# 訂單管理系統

這個專案是一個訂單管理系統，旨在處理訂單、運送和訂單項目的資料。該系統使用適配器模式來彙整不同平台的訂單數據，提供統一的接口。

## 資料庫架構

### Order

`order` 表用於存儲訂單的基本信息。

```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    -- 其他欄位可以根據需要添加
);
```

* id: 訂單的唯一識別碼。

### Shipment

`shipment` 表用於存儲與訂單相關的運送信息。

```sql
CREATE TABLE shipments (
    order_id UUID NOT NULL,
    id UUID NOT NULL,
    shipment_status VARCHAR(50) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    PRIMARY KEY (order_id, id),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);
```

* order_id: 關聯的訂單識別碼，與 orders 表關聯，並設置為外鍵，支持級聯刪除。
* id: 運送的唯一識別碼，使用 UUID 格式。
* shipment_status: 運送的狀態，使用字串表示。
* destination: 運送目的地地址。

### Order Item

`order_item` 表用於存儲每個訂單中的具體項目。

```sql
CREATE TABLE order_items (
    shipment_id UUID NOT NULL,
    id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (shipment_id, id),
    FOREIGN KEY (shipment_id) REFERENCES shipments(id) ON DELETE CASCADE
);
```

* shipment_id: 關聯的運送識別碼，與 shipments 表關聯，並設置為外鍵，支持級聯刪除。
* id: 訂單項目的唯一識別碼，使用 UUID 格式。
* name: 訂單項目的名稱。
* price: 訂單項目的單價。
* quantity: 訂單中該項目的數量。

## 使用適配器模式(adapter)處理訂單彙整

在本系統中，我們使用適配器模式來處理不同平台的訂單數據彙整。這樣的設計具有以下特點：


統一接口: 不同平台的訂單數據可以通過統一的接口進行訪問，簡化了數據處理的複雜性。


靈活性: 當需要支持新的訂單來源時，只需實現新的適配器，而不需要修改現有的業務邏輯。


可維護性: 將不同平台的邏輯封裝在適配器中，使得系統的維護和擴展變得更加容易。


數據轉換: 適配器負責將不同格式的訂單數據轉換為統一的內部格式，確保系統內部的一致性。
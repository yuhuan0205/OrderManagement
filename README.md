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

## 隔離核心與基礎設施層

在本系統中，我們採用了分離應用程式介面層（API）、核心（core）和基礎設施（infra）層的架構設計，以實現抽象與實作的隔離。這種設計模式的主要目的是提高系統的可維護性、可擴展性和測試性。透過此方式，我們能夠達到 SOLID 原則中的幾個重要方面：

### 單一職責原則（Single Responsibility Principle, SRP）
每個層級都有其明確的職責。應用程式介面層專注於處理客戶端請求和響應，核心層負責業務邏輯，而基礎設施層則處理數據存取和外部服務的集成。這樣的分離使得每個層級都能專注於其特定的功能，降低了系統的複雜性。

### 開放-封閉原則（Open/Closed Principle, OCP）
系統的設計使得每個層級都可以獨立擴展而不需要修改現有的代碼。例如，當需要添加新的 API 端點或更改數據存取方式時，只需在相應的層級中進行修改，而不會影響到其他層級的實作。這樣的設計使得系統對於擴展是開放的，但對於修改是封閉的。

### 介面隔離原則（Interface Segregation Principle, ISP）
我們的 API 層設計遵循介面隔離原則，提供了針對特定功能的細分接口。這樣，客戶端只需依賴於它們實際需要的接口，而不必依賴於不必要的功能，從而減少了系統的耦合度。

### 依賴反轉原則（Dependency Inversion Principle, DIP）
系統的高層模組（核心層）不依賴於低層模組（基礎設施層）的具體實作，而是依賴於抽象接口。這樣的設計使得我們可以輕鬆地替換或修改基礎設施層的實作，而不會影響到核心業務邏輯。

透過這種架構設計，我們能夠構建一個靈活且易於維護的系統，並能夠快速適應不斷變化的需求，同時遵循 SOLID 原則以提升系統的整體質量。
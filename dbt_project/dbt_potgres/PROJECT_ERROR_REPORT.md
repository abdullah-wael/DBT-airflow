# DBT Project Error Report

**Project:** dbt_potgres  
**Analysis Date:** 2026-02-08  
**Report Type:** Static Analysis (No modifications made)

---

## 🔍 Executive Summary

This report documents errors and potential issues found in the dbt_potgres project through static analysis. The project has been analyzed without making any changes to the source files.

**Total Issues Found:** 4  
**Critical:** 3  
**Warning:** 1  
**Info:** 0

---

## ❌ Critical Errors

### 1. Invalid Model References in Custom Tests

**Severity:** CRITICAL  
**Files Affected:**
- [tests/order_amount_postitive.sql](file:///c:/dbt/dbt_potgres/tests/order_amount_postitive.sql)
- [tests/positive_quantity.sql](file:///c:/dbt/dbt_potgres/tests/positive_quantity.sql)
- [tests/positive_unit_price.sql](file:///c:/dbt/dbt_potgres/tests/positive_unit_price.sql)
- [tests/product_price_positive.sql](file:///c:/dbt/dbt_potgres/tests/product_price_positive.sql)

**Issue:** Custom tests are referencing raw source table names instead of dbt model refs

**Details:**

#### File: `tests/order_amount_postitive.sql`
```sql
select order_id 
from {{ref('orders')}} where
 total_amount < 0
```
**Problem:** References `{{ref('orders')}}` but there is no model called `orders`. Should reference `{{ref('stg_orders')}}` or the fact table.

---

#### File: `tests/positive_quantity.sql`
```sql
select quantity 
from {{ref('order_items')}}
where quantity < 0
```
**Problem:** References `{{ref('order_items')}}` but there is no model called `order_items`. Should reference `{{ref('stg_order_items')}}` or `{{ref('fct_order_items')}}`.

---

#### File: `tests/positive_unit_price.sql`
```sql
select unit_price
from {{ref('order_items')}}
where unit_price < 0
```
**Problem:** References `{{ref('order_items')}}` but there is no model called `order_items`. Should reference `{{ref('stg_order_items')}}` or `{{ref('fct_order_items')}}`.

---

#### File: `tests/product_price_positive.sql`
```sql
select price 
from {{ref('products')}}
where price<0
```
**Problem:** References `{{ref('products')}}` but there is no model called `products`. Should reference `{{ref('stg_products')}}` or `{{ref('dim_products')}}`.

**Impact:** These tests will fail during `dbt test` or `dbt build` commands because the referenced models don't exist.

**Recommended Fix:**
```sql
-- For order_amount_postitive.sql
select order_id 
from {{ref('stg_orders')}} 
where total_amount < 0

-- For positive_quantity.sql
select quantity 
from {{ref('fct_order_items')}}
where quantity < 0

-- For positive_unit_price.sql
select unit_price
from {{ref('fct_order_items')}}
where unit_price < 0

-- For product_price_positive.sql
select price 
from {{ref('dim_products')}}
where price < 0
```

---

### 2. Missing `price` Column in Model

**Severity:** CRITICAL  
**File:** [models/marts/dim_products.sql](file:///c:/dbt/dbt_potgres/models/marts/dim_products.sql)

**Issue:** The `dim_products` model does not select the `price` column, but the test `product_price_positive.sql` expects it.

**Current Code:**
```sql
select id as product_id
,trim(name) as Product_name
,trim(category) as Product_category
from {{ref('stg_products')}}
```

**Problem:** The `price` column from `stg_products` is not being selected, so the test `product_price_positive.sql` will fail.

**Recommended Fix:**
```sql
select id as product_id
,trim(name) as Product_name
,trim(category) as Product_category
,price as Product_price  -- Add this line
from {{ref('stg_products')}}
```

---

### 3. Typo in Test Filename

**Severity:** WARNING  
**File:** [tests/order_amount_postitive.sql](file:///c:/dbt/dbt_potgres/tests/order_amount_postitive.sql)

**Issue:** Filename has a typo: "postitive" should be "positive"

**Impact:** While not a functional error, this inconsistency can cause confusion and makes the codebase less professional.

**Recommended Action:** Rename file to `order_amount_positive.sql`

---

## ⚠️ Code Quality Issues

### 1. Inconsistent Column Naming Convention

**Severity:** WARNING  
**Files Affected:** Multiple model files

**Issue:** Mix of `snake_case` and `PascalCase` in column aliases

**Examples:**

#### File: `dim_customers.sql`
```sql
select id as customer_id
, name as Full_name       -- PascalCase
,trim(email) as Email     -- PascalCase
,trim(country) as Country -- PascalCase
from {{ref('stg_customers')}}
```

#### File: `fct_order_items.sql`
```sql
select id as Order_items_id  -- PascalCase
,oi.order_id as Order_id,    -- PascalCase
-- ...mixed naming
```

**Recommended Convention:** Use consistent `snake_case` for all column names (dbt best practice)

```sql
-- dim_customers.sql
select id as customer_id
, name as full_name
,trim(email) as email
,trim(country) as country
from {{ref('stg_customers')}}

-- fct_order_items.sql
select id as order_items_id
,oi.order_id as order_id
-- etc.
```

---

### 2. Inconsistent Spacing and Formatting

**Severity:** INFO  
**Files Affected:** Multiple SQL files

**Issue:** Inconsistent comma placement and spacing

**Examples:**
```sql
-- Mixed comma placement
select id as customer_id
, name as Full_name        -- comma at start
,trim(email) as Email      -- no space before comma
```

**Recommendation:** Use consistent formatting (SQLFluff can help enforce this):
```sql
select 
    id as customer_id,
    name as full_name,
    trim(email) as email,
    trim(country) as country
from {{ref('stg_customers')}}
```

---

## ✅ Project Structure Analysis

### Models Structure
```
models/
├── staging/
│   ├── stg_customers.sql      ✅ Valid
│   ├── stg_orders.sql         ✅ Valid
│   ├── stg_order_items.sql    ✅ Valid
│   └── stg_products.sql       ✅ Valid
├── marts/
│   ├── dim_customers.sql      ⚠️ Naming inconsistency
│   ├── dim_date.sql           ✅ Valid
│   ├── dim_products.sql       ❌ Missing price column
│   └── fct_order_items.sql    ⚠️ Naming inconsistency
└── project.yml                ✅ Valid source definitions
```

### Configuration Files
- [dbt_project.yml](file:///c:/dbt/dbt_potgres/dbt_project.yml) ✅ Valid YAML syntax
- [models/project.yml](file:///c:/dbt/dbt_potgres/models/project.yml) ✅ Valid source definitions

---

## 📋 Recommended Action Plan

1. **Fix Critical Test References** (Priority: HIGHEST)
   - Update all test files to reference correct dbt models
   - Add `price` column to `dim_products` model

2. **Fix Typo** (Priority: HIGH)
   - Rename `order_amount_postitive.sql` → `order_amount_positive.sql`

3. **Standardize Naming Convention** (Priority: MEDIUM)
   - Convert all column aliases to `snake_case`
   - Update all model files for consistency

4. **Improve Code Formatting** (Priority: LOW)
   - Apply consistent SQL formatting
   - Consider using SQLFluff for automated formatting

---

## 🔧 Validation Commands

After fixes are applied, run these commands to validate:

```bash
# Parse and compile all models
dbt compile

# Run all tests
dbt test

# Build all models and run tests
dbt build

# Run specific tests
dbt test --select test_type:singular
```

---

## 📝 Notes

- This analysis was performed statically without running dbt commands
- Some issues may only be detectable during actual compilation/execution
- All referenced models and sources appear to be properly configured in YAML files
- The project follows a good structure with staging and marts layers

---

**Report Generated By:** DBT Static Analyzer  
**No changes were made to project files during this analysis**

# Data Dictionary

This dictionary defines the public demo schema for Jewelry Supply Chain Analytics with AI Insight Assistant. Public files must use anonymized sample data only.

| Field | 中文含义 | English meaning | Data type | 是否可公开 | 脱敏建议 |
| --- | --- | --- | --- | --- | --- |
| year_month | 年月 | Reporting month | string or date period, `YYYY-MM` | 可公开 | 保留年月粒度；如有商业敏感性，可平移月份或仅保留相对月份。 |
| sku_id | SKU 编号 | Anonymized SKU identifier | string | 可公开，仅限脱敏后 | 使用 `SKU_000001` 格式重新编号，不保留真实 SKU。 |
| factory_type | 工厂类型 | Generalized factory ownership or sourcing type | category/string | 可公开 | 公开样例仅使用 `In-house`、`External`、`Partner`、`Unknown`、`Other`。 |
| factory | 工厂 | Anonymized factory name | string | 可公开，仅限脱敏后 | 使用 `Factory_001` 格式替换真实工厂名称。 |
| product_category | 管理大类 | Generalized public product category | category/string | 可公开 | 公开样例仅使用 `Gem-set Jewelry`、`K-Gold & Platinum`、`Gold Jewelry`、`Fixed-price Gold`、`Unknown`、`Other`。 |
| product_series | 产品系列 | Anonymized product series | category/string | 可公开，仅限脱敏后 | 使用 `Series_001` 格式重新编号，避免真实品牌、联名或未发布系列。 |
| labor_unit_price | 起货工值单价 | Labor value per delivered unit | numeric/decimal | 视情况公开 | 可按统一比例缩放或分箱，保留相对分析关系。 |
| sku_source | SKU 来源 | Generalized SKU sourcing or creation source | category/string | 可公开 | 公开样例仅使用 `Internal Design`、`External Purchase`、`Customer Order`、`Unknown`、`Other`。 |
| monthly_order_qty | 月发单件数 | Monthly order quantity | integer | 可公开，仅限脱敏后 | 可按统一比例缩放、四舍五入或加入轻微噪声。 |
| monthly_delivery_qty | 月起货件数 | Monthly delivery quantity | integer | 可公开，仅限脱敏后 | 与订单量使用同一脱敏策略，避免逆推出真实规模。 |
| monthly_delivery_labor_value | 月起货工值 | Monthly delivered labor value | numeric/decimal | 可公开，仅限脱敏后 | 建议统一比例缩放，保留趋势和占比，不暴露真实金额/工值。 |
| product_description | 产品描述 | Product description | string | 不公开 | 从 public sample data 中删除，避免泄露客户、品牌、专利、未发布款式信息。 |
| image_path | 图片路径 | Product image path | string/path | 不公开 | 从 public sample data 中删除；不要提交真实图片路径、产品图片或内部资源链接。 |

# Data Dictionary

This dictionary defines the public demo schema for Jewelry Supply Chain Analytics with AI Insight Assistant. Public files must use anonymized sample data only.

| Field | 中文含义 | English meaning | Data type | 是否可公开 | 脱敏建议 |
| --- | --- | --- | --- | --- | --- |
| year_month | 年月 | Reporting month | string or date period, `YYYY-MM` | 可公开 | 保留年月粒度；如有商业敏感性，可平移月份或仅保留相对月份。 |
| sku_id | SKU 编号 | Anonymized SKU identifier | string | 可公开，仅限脱敏后 | 使用 `SKU_000001` 格式重新编号，不保留真实 SKU。 |
| factory_type | 工厂类型 | Factory ownership or sourcing type | category/string | 可公开 | 使用通用分类，例如 `In-house`、`External`，避免暴露组织细节。 |
| factory | 工厂 | Anonymized factory name | string | 可公开，仅限脱敏后 | 使用 `Factory_001` 格式替换真实工厂名称。 |
| product_category | 管理大类 | Management product category | category/string | 可公开 | 使用泛化后的业务分类；必要时合并小众或敏感类别。 |
| product_series | 产品系列 | Product series or collection | category/string | 可公开 | 使用泛化系列名，例如 `Series_A`；避免真实品牌、联名或未发布系列。 |
| labor_unit_price | 起货工值单价 | Labor value per delivered unit | numeric/decimal | 视情况公开 | 可按统一比例缩放或分箱，保留相对分析关系。 |
| sku_source | SKU 来源 | SKU sourcing or creation source | category/string | 可公开 | 使用通用来源标签，例如 `New Design`、`Carryover`、`Custom`。 |
| monthly_order_qty | 月发单件数 | Monthly order quantity | integer | 可公开，仅限脱敏后 | 可按统一比例缩放、四舍五入或加入轻微噪声。 |
| monthly_delivery_qty | 月起货件数 | Monthly delivery quantity | integer | 可公开，仅限脱敏后 | 与订单量使用同一脱敏策略，避免逆推出真实规模。 |
| monthly_delivery_labor_value | 月起货工值 | Monthly delivered labor value | numeric/decimal | 可公开，仅限脱敏后 | 建议统一比例缩放，保留趋势和占比，不暴露真实金额/工值。 |
| product_description | 产品描述 | Product description | string | 谨慎公开 | 删除客户、品牌、专利、未发布款式信息；可改写为通用描述。 |
| image_path | 图片路径 | Product image path | string/path | 不公开 | 公开样例中移除或置空；不要提交真实图片路径或内部资源链接。 |


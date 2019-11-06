import pandas as pd
from dask import dataframe as dd

import featuretools as ft
from featuretools.entityset import EntitySet


def test_create_entity_from_dask_df(es):
    log_dask = dd.from_pandas(es["log"].df, npartitions=2)
    es = es.entity_from_dataframe(
        entity_id="log_dask",
        dataframe=log_dask,
        index="id",
        time_index="datetime",
        variable_types=es["log"].variable_types
    )

    assert es["log"].df.equals(es["log_dask"].df.compute())


# def test_single_table_entityset():
#     es = EntitySet(id="es")
#     values = pd.DataFrame({"id": [1, 0, 2, 3], "values": [1, 12, 34, 27]})
#     es.entity_from_dataframe(entity_id="data",
#                              dataframe=values,
#                              index="id")

#     fm, _ = ft.dfs(entityset=es,
#                    target_entity="data",
#                    trans_primitives=['cum_sum'],
#                    max_depth=1,
#                    chunk_size=2)

#     print(fm)


def test_single_table_entityset_dask():
    dask_es = EntitySet(id="dask_es")
    df = pd.DataFrame({"id": [0, 1, 2, 3], "values": [1, 12, 34, 27]})
    values_dd = dd.from_pandas(df, npartitions=4)
    dask_es.entity_from_dataframe(entity_id="data",
                                  dataframe=values_dd,
                                  index="id")

    dask_fm, _ = ft.dfs(entityset=dask_es,
                        target_entity="data",
                        trans_primitives=['cum_sum'],
                        max_depth=1)

    es = ft.EntitySet(id="es")
    es.entity_from_dataframe(entity_id="data",
                             dataframe=df,
                             index="id")

    fm, _ = ft.dfs(entityset=es,
                   target_entity="data",
                   trans_primitives=['cum_sum'],
                   max_depth=1)

    assert fm.equals(dask_fm.compute())


# def test_single_table_entityset_dask_unordered_ids():
#     dask_es = EntitySet(id="dask_es")
#     df = pd.DataFrame({"id": [1, 0, 3, 2], "values": [1, 12, 34, 27]})
#     values_dd = dd.from_pandas(df, npartitions=4)
#     dask_es.entity_from_dataframe(entity_id="data",
#                                   dataframe=values_dd,
#                                   index="id")

#     dask_fm, _ = ft.dfs(entityset=dask_es,
#                         target_entity="data",
#                         trans_primitives=['cum_sum'],
#                         max_depth=1)

#     es = ft.EntitySet(id="es")
#     es.entity_from_dataframe(entity_id="data",
#                              dataframe=df,
#                              index="id")

#     fm, _ = ft.dfs(entityset=es,
#                    target_entity="data",
#                    trans_primitives=['cum_sum'],
#                    max_depth=1)

#     assert fm.equals(dask_fm.compute())


# def test_build_es_from_scratch():
#     es = ft.demo.load_mock_customer(return_entityset=True)
#     data = ft.demo.load_mock_customer()
#
#     transactions_df = data["transactions"].merge(data["sessions"]).merge(data["customers"])
#     transactions_dd = dd.from_pandas(transactions_df, npartitions=4)
#     products_dd = dd.from_pandas(data["products"], npartitions=4)
#
#     dask_es = EntitySet(id="dask_es")
#     dask_es.entity_from_dataframe(entity_id="transactions",
#                                   dataframe=transactions_dd,
#                                   index="transaction_id",
#                                   time_index="transaction_time",
#                                   variable_types={"product_id": ft.variable_types.Categorical,
#                                                   "zip_code": ft.variable_types.ZIPCode})
#     dask_es.entity_from_dataframe(entity_id="products",
#                                   dataframe=products_dd,
#                                   index="product_id")
#
#     new_rel = Relationship(dask_es["products"]["product_id"],
#                            dask_es["transactions"]["product_id"])
#
#     dask_es = dask_es.add_relationship(new_rel)
#
#     dask_es = dask_es.normalize_entity(base_entity_id="transactions",
#                                        new_entity_id="sessions",
#                                        index="session_id",
#                                        make_time_index="session_start",
#                                        additional_variables=["device",
#                                                              "customer_id",
#                                                              "zip_code",
#                                                              "session_start",
#                                                              "join_date"])
#
#     dask_es = dask_es.normalize_entity(base_entity_id="sessions",
#                                        new_entity_id="customers",
#                                        index="customer_id",
#                                        make_time_index="join_date",
#                                        additional_variables=["zip_code", "join_date"])
#
#     fm, _ = ft.dfs(entityset=es,
#                    target_entity="products",
#                    max_depth=1)
#
#     feature_matrix, feature_defs = ft.dfs(entityset=dask_es,
#                                           target_entity="products",
#                                           max_depth=1)
#
#

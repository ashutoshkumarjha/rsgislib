RSGISLib Data Sources
========================

This module has function to help with accessing and downloading data.


USGS Earth Explorer
---------------------

.. autofunction:: rsgislib.dataaccess.usgs_m2m.usgs_login
.. autofunction:: rsgislib.dataaccess.usgs_m2m.usgs_logout
.. autofunction:: rsgislib.dataaccess.usgs_m2m.can_user_dwnld
.. autofunction:: rsgislib.dataaccess.usgs_m2m.can_user_order
.. autofunction:: rsgislib.dataaccess.usgs_m2m.get_wrs_pt
.. autofunction:: rsgislib.dataaccess.usgs_m2m.get_wrs_bbox
.. autofunction:: rsgislib.dataaccess.usgs_m2m.usgs_search
.. autofunction:: rsgislib.dataaccess.usgs_m2m.get_all_usgs_search
.. autofunction:: rsgislib.dataaccess.usgs_m2m.get_download_ids
.. autofunction:: rsgislib.dataaccess.usgs_m2m.create_scene_list
.. autofunction:: rsgislib.dataaccess.usgs_m2m.remove_scene_list
.. autofunction:: rsgislib.dataaccess.usgs_m2m.check_dwnld_opts


NASA Common Metadata Repository
---------------------------------

.. autofunction:: rsgislib.dataaccess.nasa_cmr.get_prods_info
.. autofunction:: rsgislib.dataaccess.nasa_cmr.check_prod_version_avail
.. autofunction:: rsgislib.dataaccess.nasa_cmr.get_max_prod_version
.. autofunction:: rsgislib.dataaccess.nasa_cmr.find_granules
.. autofunction:: rsgislib.dataaccess.nasa_cmr.find_all_granules
.. autofunction:: rsgislib.dataaccess.nasa_cmr.get_total_file_size
.. autofunction:: rsgislib.dataaccess.nasa_cmr.cmr_download_file_http



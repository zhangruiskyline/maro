# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.


from functools import wraps

from maro.cli.utils.details import load_cluster_details
from maro.utils.exception.cli_exception import BadRequestError, ClusterInternalError


def check_details_validity(func):
    @wraps(func)
    def with_checker(*args, **kwargs):
        # Get params
        cluster_name = kwargs["cluster_name"]

        # Get details
        try:
            cluster_details = load_cluster_details(cluster_name=cluster_name)

            # Check details validity
            if cluster_details["mode"] not in {
                "grass/azure", "k8s/aks"
            }:
                raise ClusterInternalError(f"Cluster details are broken: Invalid mode '{cluster_details['mode']}'.")
        except FileNotFoundError:
            raise BadRequestError(f"Cluster '{cluster_name}' is not found.")
        except KeyError as e:
            raise ClusterInternalError(f"Cluster details are broken: Missing key 'mode'.")

        func(*args, **kwargs)

    return with_checker

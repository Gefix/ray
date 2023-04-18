import itertools
import unittest

from ray.rllib.core.models.configs import MLPHeadConfig, FreeLogStdMLPHeadConfig
from ray.rllib.utils.framework import try_import_torch

torch, nn = try_import_torch()


class TestTorchMLPHead(unittest.TestCase):
    def test_torch_mlp_head(self):

        inputs_dims_configs = [[1], [2], [1000]]

        list_of_hidden_layer_dims = [[], [1], [64, 64], [1000, 1000, 1000, 1000]]

        hidden_layer_activations = [None, "linear", "relu", "tanh", "elu", "swish"]

        # Can only test even output_dims for FreeLogStdMLPHeadConfig.
        output_dims_configs = [[2], [1000]]

        output_activations = hidden_layer_activations

        free_stds = [False, True]

        for permutation in itertools.product(
            inputs_dims_configs,
            list_of_hidden_layer_dims,
            hidden_layer_activations,
            output_activations,
            output_dims_configs,
            free_stds,
        ):
            (
                inputs_dims,
                hidden_layer_dims,
                hidden_layer_activation,
                output_activation,
                output_dims,
                free_std,
            ) = permutation

            print(
                f"Testing ...\n"
                f"inputs_dim: {inputs_dims}\n"
                f"hidden_layer_dims: {hidden_layer_dims}\n"
                f"hidden_layer_activation: {hidden_layer_activation}\n"
                f"output_activation: {output_activation}\n"
                f"output_dims: {output_dims}\n"
                f"free_std: {free_std}\n"
            )

            config = MLPHeadConfig(
                input_dims=inputs_dims,
                hidden_layer_dims=hidden_layer_dims,
                output_dims=output_dims,
                hidden_layer_activation=hidden_layer_activation,
                output_activation=output_activation,
            )

            if free_std:
                config = FreeLogStdMLPHeadConfig(mlp_head_config=config)

            model = config.build(framework="torch")

            inputs = torch.randn(1, inputs_dims[0])

            outputs = model(inputs)

            self.assertEqual(outputs.shape, (1, output_dims[0]))


if __name__ == "__main__":
    import pytest
    import sys

    sys.exit(pytest.main(["-v", __file__]))
from dmipy_custom.core import modeling_framework
from dmipy_custom.core.acquisition_scheme import (
    acquisition_scheme_from_bvalues)
from dmipy_custom.signal_models import (
    cylinder_models, plane_models, gaussian_models)
from numpy.testing import assert_raises
from dmipy_custom.data.saved_acquisition_schemes import (
    wu_minn_hcp_acquisition_scheme)
import numpy as np


def test_raise_combination_NRM_and_others():
    ball = gaussian_models.G1Ball()
    plane = plane_models.P3PlaneCallaghanApproximation()

    assert_raises(
        ValueError, modeling_framework.MultiCompartmentModel,
        [ball, plane])


def test_raise_NRMmodel_in_spherical_mean():
    plane = plane_models.P3PlaneCallaghanApproximation()
    assert_raises(
        ValueError,
        modeling_framework.MultiCompartmentSphericalMeanModel,
        [plane])


def test_raise_mix_with_tortuosity_in_mcsmtmodel():
    scheme = wu_minn_hcp_acquisition_scheme()
    stick = cylinder_models.C1Stick()
    zeppelin = gaussian_models.G2Zeppelin()
    mcsmt = modeling_framework.MultiCompartmentSphericalMeanModel(
        [stick, zeppelin])
    mcsmt.set_tortuous_parameter(
        'G2Zeppelin_1_lambda_perp',
        'C1Stick_1_lambda_par',
        'partial_volume_0',
        'partial_volume_1')

    data = stick(scheme, lambda_par=1.7e-9, mu=[0., 0.])

    assert_raises(ValueError, mcsmt.fit, scheme, data, solver='mix')


def test_raise_mix_with_tortuosity_in_mcmodel():
    scheme = wu_minn_hcp_acquisition_scheme()
    stick = cylinder_models.C1Stick()
    zeppelin = gaussian_models.G2Zeppelin()
    mc = modeling_framework.MultiCompartmentModel(
        [stick, zeppelin])
    mc.set_tortuous_parameter(
        'G2Zeppelin_1_lambda_perp',
        'C1Stick_1_lambda_par',
        'partial_volume_0',
        'partial_volume_1')

    data = stick(scheme, lambda_par=1.7e-9, mu=[0., 0.])

    assert_raises(ValueError, mc.fit, scheme, data, solver='mix')


def test_set_fixed_parameter_raises():
    cyl = cylinder_models.C1Stick()
    mod = modeling_framework.MultiCompartmentModel([cyl])
    assert_raises(ValueError, mod.set_fixed_parameter,
                  'C1Stick_1_mu', [1])
    assert_raises(ValueError, mod.set_fixed_parameter,
                  'blabla', [1])


def test_wrong_number_S0_tissue_responses_raises():
    cyl = cylinder_models.C1Stick()
    mods = [cyl]
    S0s = [1., 1.]
    assert_raises(
        ValueError,
        modeling_framework.MultiCompartmentModel, mods, S0s)
    assert_raises(
        ValueError,
        modeling_framework.MultiCompartmentSphericalMeanModel, mods, S0s)
    assert_raises(
        ValueError,
        modeling_framework.MultiCompartmentSphericalHarmonicsModel, mods, S0s)


def test_fitting_without_b0_raises():
    bvals = np.atleast_1d(1e9)
    bvecs = np.atleast_2d([1., 0., 0.])
    scheme = acquisition_scheme_from_bvalues(bvals, bvecs)
    mc = modeling_framework.MultiCompartmentModel(
        [gaussian_models.G1Ball()])
    data = np.atleast_1d(1.)
    assert_raises(ValueError, mc.fit, scheme, data)


def test_set_parameter_optimization_bounds_raises():
    ball = gaussian_models.G1Ball()
    mc = modeling_framework.MultiCompartmentModel([ball])
    assert_raises(ValueError, mc.set_parameter_optimization_bounds,
                  'not a valid name', [1, 2])
    assert_raises(ValueError, mc.set_parameter_optimization_bounds,
                  'G1Ball_1_lambda_iso', 1)
    assert_raises(ValueError, mc.set_parameter_optimization_bounds,
                  'G1Ball_1_lambda_iso', [[1, 2], [1, 2]])
    assert_raises(ValueError, mc.set_parameter_optimization_bounds,
                  'G1Ball_1_lambda_iso', [1, 2, 3])
    assert_raises(ValueError, mc.set_parameter_optimization_bounds,
                  'G1Ball_1_lambda_iso', [2, 1])

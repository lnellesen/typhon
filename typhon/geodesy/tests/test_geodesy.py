# -*- coding: utf-8 -*-

"""Testing the basic geodetic functions.
"""

import numpy as np

from typhon import geodesy


class TestConversion(object):
    """Testing the geodetic conversion functions.

    This class provides functions to test the conversion between different
    coordinate systems.
    """
    def test_ellipsoidmodels(self):
        """Check ellipsoidmodels for valid excentricities."""
        e = geodesy.ellipsoidmodels()

        exc = np.array([e[m][1] for m in e.models])

        assert (np.all(exc >= 0) and np.all(exc < 1))

    def test_cart2geocentric(self):
        """Test conversion from cartesian to geocentric system."""
        cartesian = (np.array([1, 0, 0]),  # x
                     np.array([0, 1, 0]),  # y
                     np.array([0, 0, 1]),  # z
                     )

        reference = (np.array([1, 1, 1]),  # r
                     np.array([0, 0, 90]),  # lat
                     np.array([0, 90, 0]),  # lon
                     )

        conversion = geodesy.cart2geocentric(*cartesian)

        assert np.allclose(conversion, reference)

    def test_geocentric2cart(self):
        """Test conversion from cartesian to geocentric system."""
        geocentric = (np.array([1, 1, 1]),  # r
                      np.array([0, 0, 90]),  # lat
                      np.array([0, 90, 0]),  # lon
                      )

        reference = (np.array([1, 0, 0]),  # x
                     np.array([0, 1, 0]),  # y
                     np.array([0, 0, 1]),  # z
                     )

        conversion = geodesy.geocentric2cart(*geocentric)

        assert np.allclose(conversion, reference)

    def test_geocentric2cart2geocentric(self):
        """Test conversion from geocentric to cartesian system and back."""
        ref = (1, -13, 42)

        cart = geodesy.geocentric2cart(*ref)
        geo = geodesy.cart2geocentric(*cart)

        assert np.allclose(ref, geo)

    def test_geodetic2cart2geodetic(self):
        """Test geodetic/cartesian conversion for all ellipsoids."""
        e = geodesy.ellipsoidmodels()

        for model in e.models:
            yield self._geodetic2cart2geodetic, e[model]

    def _geodetic2cart2geodetic(self, ellipsoid):
        """Test conversion from geodetic to cartesian system and back."""
        ref = (1, -13, 42)

        cart = geodesy.geodetic2cart(*ref, ellipsoid)
        geod = geodesy.cart2geodetic(*cart, ellipsoid)

        assert np.allclose(ref, geod)

    def test_geodetic2geocentric2geodetic(self):
        """Test geodetic/geocentric conversion for all ellipsoids."""
        e = geodesy.ellipsoidmodels()

        for model in e.models:
            yield self._geodetic2geocentric2geodetic, e[model]

    def _geodetic2geocentric2geodetic(self, ellipsoid):
        """Test conversion from geodetic to geocentric system and back."""
        ref = (1, -13, 42)

        geoc = geodesy.geodetic2geocentric(*ref, ellipsoid)
        geod = geodesy.geocentric2geodetic(*geoc, ellipsoid)

        assert np.allclose(ref, geod)

    # TODO: Consider if it is useful to check ellisoir_r_* calculation for
    # *all* ellipsoid models.
    # TODO: Both tests are currently only checking the easy way of the
    # function's alrogithm.
    def test_ellipsoid_r_geodetic(self):
        """Test return of geodetic radius for all ellipsois."""
        e = geodesy.ellipsoidmodels()

        for model in e.models:
            yield self._geodetic_r_at_equator, e[model]

    def _geodetic_r_at_equator(self, ellipsoid):
        """Check the geodetic radius at equator."""
        r = geodesy.ellipsoid_r_geodetic(ellipsoid, 0)

        # Radius at equator has to be equal to the one defined in the
        # ellipsoidmodel.
        assert ellipsoid[0] == r

    def test_ellipsoid_r_geocentric(self):
        """Test return of geocentric radius for all ellipsois."""
        e = geodesy.ellipsoidmodels()

        for model in e.models:
            yield self._geocentric_r_at_equator, e[model]

    def _geocentric_r_at_equator(self, ellipsoid):
        """Check the geocentric radius at equator."""
        r = geodesy.ellipsoid_r_geocentric(ellipsoid, 0)

        # Radius at equator has to be equal to the one defined in the
        # ellipsoidmodel.
        assert ellipsoid[0] == r

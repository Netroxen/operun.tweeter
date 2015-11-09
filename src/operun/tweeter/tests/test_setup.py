# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from operun.tweeter.testing import OPERUN_TWEETER_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that operun.tweeter is properly installed."""

    layer = OPERUN_TWEETER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if operun.tweeter is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'operun.tweeter'))

    def test_browserlayer(self):
        """Test that IOperunTweeterLayer is registered."""
        from operun.tweeter.interfaces import (
            IOperunTweeterLayer)
        from plone.browserlayer import utils
        self.assertIn(IOperunTweeterLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = OPERUN_TWEETER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['operun.tweeter'])

    def test_product_uninstalled(self):
        """Test if operun.tweeter is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'operun.tweeter'))

    def test_browserlayer_removed(self):
        """Test that IOperunTweeterLayer is removed."""
        from operun.tweeter.interfaces import IOperunTweeterLayer
        from plone.browserlayer import utils
        self.assertNotIn(IOperunTweeterLayer, utils.registered_layers())

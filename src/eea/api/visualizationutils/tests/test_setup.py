# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from eea.api.visualizationutils.testing import (  # noqa: E501
    EEA_API_VISUALIZATIONUTILS_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that eea.api.visualizationutils is properly installed."""

    layer = EEA_API_VISUALIZATIONUTILS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if eea.api.visualizationutils is installed."""
        self.assertTrue(
            self.installer.is_product_installed("eea.api.visualizationutils")
        )

    def test_browserlayer(self):
        """Test that IEeaApiVisualizationutilsLayer is registered."""
        from eea.api.visualizationutils.interfaces import IEeaApiVisualizationutilsLayer
        from plone.browserlayer import utils

        self.assertIn(IEeaApiVisualizationutilsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = EEA_API_VISUALIZATIONUTILS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("eea.api.visualizationutils")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if eea.api.visualizationutils is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("eea.api.visualizationutils")
        )

    def test_browserlayer_removed(self):
        """Test that IEeaApiVisualizationutilsLayer is removed."""
        from eea.api.visualizationutils.interfaces import IEeaApiVisualizationutilsLayer
        from plone.browserlayer import utils

        self.assertNotIn(IEeaApiVisualizationutilsLayer, utils.registered_layers())

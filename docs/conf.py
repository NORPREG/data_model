import os
import sys
sys.path.insert(0, os.path.abspath('../model/'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Datamodell for NORPREG'
copyright = '2026, Helge Pettersen'
author = 'Helge Pettersen'
release = '0.9'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinxcontrib.autodoc_pydantic'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'undoc-members': True,
    'ignore-module-all': False,
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = 'static/norpreg_logo.png'


autodoc_pydantic_model_show_json = True
autodoc_pydantic_model_show_config_list = True
autodoc_pydantic_model_show_field_summary = True
autodoc_pydantic_model_show_field_list = True
autodoc_pydantic_model_member_order = "bysource"
autodoc_pydantic_field_doc_policy = "both"
autodoc_pydantic_field_swap_name_and_alias = True
autodoc_pydantic_field_show_alias = True
autodoc_pydantic_field_list_validators = True
autodoc_pydantic_model_hide_paramlist = False
autodoc_pydantic_settings_hide_paramlist = False
autodoc_pydantic_model_show_validator_summary = True

autodoc_pydantic_model_show_config_summary = True
autodoc_pydantic_model_show_config_members = True
autodoc_pydantic_model_show_validator_members = True
autodoc_pydantic_model_hide_reused_validator = True
autodoc_pydantic_field_show_required = True
autodoc_pydantic_field_show_default = True
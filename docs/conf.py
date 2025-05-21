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
copyright = '2025, Helge Pettersen'
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

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


autodoc_pydantic_model_show_json = True  # Skru av JSON-visning hvis ikke ønskelig
autodoc_pydantic_model_show_config_list = False
autodoc_pydantic_model_show_field_summary = False
autodoc_pydantic_model_show_field_list = True
autodoc_pydantic_model_member_order = "bysource"
autodoc_pydantic_field_doc_policy = "description"
autodoc_pydantic_field_swap_name_and_alias = False
autodoc_pydantic_field_show_alias = False
autodoc_pydantic_field_list_validators = True
autodoc_pydantic_model_hide_paramlist = True
autodoc_pydantic_settings_hide_paramlist = True
autodoc_pydantic_model_show_validator_summary = False

autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_config_members = False
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_model_hide_reused_validator = True
autodoc_pydantic_field_show_required = False
autodoc_pydantic_field_show_default = False
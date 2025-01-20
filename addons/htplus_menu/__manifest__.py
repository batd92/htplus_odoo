{
    "name": "HTPlus Menu",
    "version": "1.1.0",
    "summary": "Enhanced navigation module for Odoo Community Edition.",
    "description": """
        This module offers a centralized main menu specifically designed for the Odoo Community Edition, developed by HTPlus.
    """,
    "author": "Ba.TD",
    "maintainer": "Ba.TD",
    "website": "",
    "license": "LGPL-3",
    "category": "HTPlus",
    "depends": [
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/main_menu_views.xml",
        "views/menu_bookmark_views.xml",
        "views/res_config_setting_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "htplus_menu/static/src/components/**/*",
        ],
    },
    "images": [
        "static/description/banner.png",
    ],
    "auto_install": True,
    "application": True,
    "installable": True,
}

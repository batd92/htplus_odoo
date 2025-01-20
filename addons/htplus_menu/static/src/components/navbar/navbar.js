import { patch } from "@web/core/utils/patch";
import { NavBar } from "@web/webclient/navbar/navbar";

patch(NavBar.prototype, {
    setup() {
        super.setup();

        const root = this.menuService.getMenuAsTree("root").childrenTree;
        this.menuApp = root.find(app => app.xmlid === "htplus_menu.main_menu_root");
    },

    onClickMenu() {
        if (this.menuApp && !this._isMainMenu()) {
            this._onMenuClicked(this.menuApp);
        }
    },
    _isMainMenu() {
        const currentApp = this.menuService.getCurrentApp();
        return currentApp && currentApp.xmlid === 'htplus_menu.main_menu_root';
    }
});

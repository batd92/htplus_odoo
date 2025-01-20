import { Component, onWillStart, useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { standardActionServiceProps } from "@web/webclient/actions/action_service";

class MenuAction extends Component {
    static props = {...standardActionServiceProps};
    static template = "htplus_menu.MainMenu";

    setup() {

        // state
        this.state = { isOpen: true };
        this.commandPaletteOpen = false;

        this.orm = useService("orm");
        this.menuService = useService("menu");
        const companyService = useService("company");
        this.commandService = useService("command");

        this.currentCompanyId = companyService.currentCompany.id
        this.apps = this.menuService.getApps()
                        .filter(app => app.xmlid != "htplus_menu.main_menu_root")
                        //.sort((a, b) => a.name.localeCompare(b.name));

        this.deg = `${90 + 180 * Math.atan(window.innerHeight / window.innerWidth) / Math.PI}deg`;

        onWillStart(async () => {
            try {
                this.userIsAdmin = await user.hasGroup("base.group_system");
            } catch (error) {
                console.error("Error loading data:", error);
            }
        });

        useEffect(
            (isOpen) => {
            	if (isOpen) {
            		const openMainPalette = (ev) => {
            	    	if (
            	    		!this.commandServiceOpen && 
            	    		ev.key.length === 1 &&
            	    		!ev.ctrlKey &&
            	    		!ev.altKey
            	    	) {
	            	        this.commandService.openMainPalette(
            	        		{ searchValue: `/${ev.key}` }, 
            	        		() => { this.commandPaletteOpen = false; }
            	        	);
	            	    	this.commandPaletteOpen = true;
            	    	}
            		}
	            	window.addEventListener("keydown", openMainPalette);
	                return () => {
	                	window.removeEventListener("keydown", openMainPalette);
	                	this.commandPaletteOpen = false;
	                }
            	}
            },
            () => [this.state.isOpen]
		);
    }

    onClickModule(menu) {
        console.log('this.onClickMenu 000');
        menu && this.menuService.selectMenu(menu);
    }

    async onSaveAnnouncement(){
        try {
            await this.orm.write("res.company", [this.currentCompanyId], {
                "announcement": this.announcement
            });
        } catch (error) {
            console.error("Error saving data:", error);
        }
    }
}

registry
    .category("actions")
    .add("main_menu.action_open_main_menu", MenuAction);


/* /web/static/src/polyfills/object.js */
if(!Object.hasOwn){Object.hasOwn=(obj,key)=>Object.prototype.hasOwnProperty.call(obj,key);};

/* /web/static/src/polyfills/array.js */
if(!Array.prototype.at){Object.defineProperty(Array.prototype,"at",{enumerable:false,value:function(index){if(index>=0){return this[index];}
return this[this.length+index];}});};

/* /web/static/src/module_loader.js */
(function(odoo){"use strict";if(odoo.loader){return;}
class ModuleLoader{bus=new EventTarget();checkErrorProm=null;factories=new Map();failed=new Set();jobs=new Set();modules=new Map();constructor(root){this.root=root;}
addJob(name){this.jobs.add(name);this.startModules();}
define(name,deps,factory,lazy=false){if(typeof name!=="string"){throw new Error(`Module name should be a string, got: ${String(name)}`);}
if(!Array.isArray(deps)){throw new Error(`Module dependencies should be a list of strings, got: ${String(deps)}`);}
if(typeof factory!=="function"){throw new Error(`Module factory should be a function, got: ${String(factory)}`);}
if(this.factories.has(name)){return;}
this.factories.set(name,{deps,fn:factory,ignoreMissingDeps:globalThis.__odooIgnoreMissingDependencies,});if(!lazy){this.addJob(name);this.checkErrorProm||=Promise.resolve().then(()=>{this.checkErrorProm=null;this.reportErrors(this.findErrors());});}}
findErrors(moduleNames){const findCycle=(currentModuleNames,visited)=>{for(const name of currentModuleNames||[]){if(visited.has(name)){const cycleModuleNames=[...visited,name];return cycleModuleNames.slice(cycleModuleNames.indexOf(name)).map((j)=>`"${j}"`).join(" => ");}
const cycle=findCycle(dependencyGraph[name],new Set(visited).add(name));if(cycle){return cycle;}}
return null;};moduleNames||=this.jobs;const dependencyGraph=Object.create(null);const missing=new Set();const unloaded=new Set();for(const moduleName of moduleNames){const{deps,ignoreMissingDeps}=this.factories.get(moduleName);dependencyGraph[moduleName]=deps;if(ignoreMissingDeps){continue;}
unloaded.add(moduleName);for(const dep of deps){if(!this.factories.has(dep)){missing.add(dep);}}}
const cycle=findCycle(moduleNames,new Set());const errors={};if(cycle){errors.cycle=cycle;}
if(this.failed.size){errors.failed=this.failed;}
if(missing.size){errors.missing=missing;}
if(unloaded.size){errors.unloaded=unloaded;}
return errors;}
findJob(){for(const job of this.jobs){if(this.factories.get(job).deps.every((dep)=>this.modules.has(dep))){return job;}}
return null;}
async reportErrors(errors){if(!Object.keys(errors).length){return;}
const document=this.root?.ownerDocument||globalThis.document;if(document.readyState==="loading"){await new Promise((resolve)=>document.addEventListener("DOMContentLoaded",resolve));}
this.root||=document.body;const containerEl=document.createElement("div");containerEl.className="o_module_error position-fixed w-100 h-100 d-flex align-items-center flex-column bg-white overflow-auto modal";containerEl.style.zIndex="10000";const alertEl=document.createElement("div");alertEl.className="alert alert-danger o_error_detail fw-bold m-auto";containerEl.appendChild(alertEl);const errorHeadings=[];if(errors.failed){errorHeadings.push(["The following modules failed to load because of an error, you may find more information in the devtools console:",[...errors.failed],]);}
if(errors.cycle){errorHeadings.push(["The following modules could not be loaded because they form a dependency cycle:",[errors.cycle],]);}
if(errors.missing){errorHeadings.push(["The following modules are needed by other modules but have not been defined, they may not be present in the correct asset bundle:",[...errors.missing],]);}
if(errors.unloaded){errorHeadings.push(["The following modules could not be loaded because they have unmet dependencies, this is a secondary error which is likely caused by one of the above problems:",[...errors.unloaded],]);}
for(const[heading,moduleNames]of errorHeadings){const listEl=document.createElement("ul");for(const moduleName of moduleNames){const listItemEl=document.createElement("li");listItemEl.textContent=moduleName;listEl.appendChild(listItemEl);}
alertEl.appendChild(document.createTextNode(heading));alertEl.appendChild(listEl);}
this.root.innerHTML="";this.root.appendChild(containerEl);}
startModules(){let job;while((job=this.findJob())){this.startModule(job);}}
startModule(name){const require=(dependency)=>this.modules.get(dependency);this.jobs.delete(name);const factory=this.factories.get(name);let module=null;try{module=factory.fn(require);}catch(error){this.failed.add(name);throw new Error(`Error while loading "${name}":\n${error}`);}
this.modules.set(name,module);this.bus.dispatchEvent(new CustomEvent("module-started",{detail:{moduleName:name,module},}));return module;}}
if(odoo.debug&&!new URLSearchParams(location.search).has("debug")){odoo.debug="";}
const loader=new ModuleLoader();odoo.define=loader.define.bind(loader);odoo.loader=loader;})((globalThis.odoo||={}));;

/* /web/static/src/session.js */
odoo.define('@web/session',[],function(require){'use strict';let __exports={};const session=__exports.session=odoo.__session_info__||{};delete odoo.__session_info__;return __exports;});;

/* /web/static/src/core/browser/cookie.js */
odoo.define('@web/core/browser/cookie',[],function(require){'use strict';let __exports={};const COOKIE_TTL=24*60*60*365;const cookie=__exports.cookie={get _cookieMonster(){return document.cookie;},set _cookieMonster(value){document.cookie=value;},get(str){const parts=this._cookieMonster.split("; ");for(const part of parts){const[key,value]=part.split(/=(.*)/);if(key===str){return value||"";}}},set(key,value,ttl=COOKIE_TTL){let fullCookie=[];if(value!==undefined){fullCookie.push(`${key}=${value}`);}
fullCookie=fullCookie.concat(["path=/",`max-age=${ttl}`]);this._cookieMonster=fullCookie.join("; ");},delete(key){this.set(key,"kill",0);},};return __exports;});;

/* /web/static/src/core/utils/ui.js */
odoo.define('@web/core/utils/ui',[],function(require){'use strict';let __exports={};__exports.closest=closest;function closest(elements,targetPos){let closestEl=null;let closestDistance=Infinity;for(const el of elements){const rect=el.getBoundingClientRect();const distance=getQuadrance(rect,targetPos);if(!closestEl||distance<closestDistance){closestEl=el;closestDistance=distance;}}
return closestEl;}
__exports.isVisible=isVisible;function isVisible(el){if(el===document||el===window){return true;}
if(!el){return false;}
let _isVisible=false;if("offsetWidth"in el&&"offsetHeight"in el){_isVisible=el.offsetWidth>0&&el.offsetHeight>0;}else if("getBoundingClientRect"in el){const rect=el.getBoundingClientRect();_isVisible=rect.width>0&&rect.height>0;}
if(!_isVisible&&getComputedStyle(el).display==="contents"){for(const child of el.children){if(isVisible(child)){return true;}}}
return _isVisible;}
__exports.getQuadrance=getQuadrance;function getQuadrance(rect,pos){let q=0;if(pos.x<rect.x){q+=(rect.x-pos.x)**2;}else if(rect.x+rect.width<pos.x){q+=(pos.x-(rect.x+rect.width))**2;}
if(pos.y<rect.y){q+=(rect.y-pos.y)**2;}else if(rect.y+rect.height<pos.y){q+=(pos.y-(rect.y+rect.height))**2;}
return q;}
__exports.getVisibleElements=getVisibleElements;function getVisibleElements(activeElement,selector){const visibleElements=[];const elements=activeElement.querySelectorAll(selector);for(const el of elements){if(isVisible(el)){visibleElements.push(el);}}
return visibleElements;}
__exports.touching=touching;function touching(elements,targetRect){const r1={x:0,y:0,width:0,height:0,...targetRect};return[...elements].filter((el)=>{const r2=el.getBoundingClientRect();return(r2.x+r2.width>=r1.x&&r2.x<=r1.x+r1.width&&r2.y+r2.height>=r1.y&&r2.y<=r1.y+r1.height);});}
const TABABLE_SELECTOR=["[tabindex]","a","area","button","frame","iframe","input","object","select","textarea","details > summary:nth-child(1)",].map((sel)=>`${sel}:not([tabindex="-1"]):not(:disabled)`).join(",");__exports.getTabableElements=getTabableElements;function getTabableElements(container=document.body){const elements=[...container.querySelectorAll(TABABLE_SELECTOR)].filter(isVisible);const byTabIndex={};for(const el of[...elements]){if(!byTabIndex[el.tabIndex]){byTabIndex[el.tabIndex]=[];}
byTabIndex[el.tabIndex].push(el);}
const withTabIndexZero=byTabIndex[0]||[];delete byTabIndex[0];return[...Object.values(byTabIndex).flat(),...withTabIndexZero];}
__exports.getNextTabableElement=getNextTabableElement;function getNextTabableElement(container=document.body){const tabableElements=getTabableElements(container);const index=tabableElements.indexOf(document.activeElement);return index===-1?tabableElements[0]:tabableElements[index+1]||null;}
__exports.getPreviousTabableElement=getPreviousTabableElement;function getPreviousTabableElement(container=document.body){const tabableElements=getTabableElements(container);const index=tabableElements.indexOf(document.activeElement);return index===-1?tabableElements[tabableElements.length-1]:tabableElements[index-1]||null;}
__exports.addLoadingEffect=addLoadingEffect;function addLoadingEffect(btnEl){btnEl.classList.add("o_btn_loading","disabled","pe-none");btnEl.disabled=true;const loaderEl=document.createElement("span");loaderEl.classList.add("fa","fa-refresh","fa-spin","me-2");btnEl.prepend(loaderEl);return()=>{btnEl.classList.remove("o_btn_loading","disabled","pe-none");btnEl.disabled=false;loaderEl.remove();};}
return __exports;});;

/* /web/static/src/legacy/js/public/minimal_dom.js */
odoo.define('@web/legacy/js/public/minimal_dom',['@web/core/utils/ui'],function(require){'use strict';let __exports={};const{addLoadingEffect}=require('@web/core/utils/ui');const DEBOUNCE=__exports.DEBOUNCE=400;const BUTTON_HANDLER_SELECTOR=__exports.BUTTON_HANDLER_SELECTOR='a, button, input[type="submit"], input[type="button"], .btn';__exports.makeAsyncHandler=makeAsyncHandler;function makeAsyncHandler(fct,preventDefault,stopPropagation,stopImmediatePropagation){let pending=false;function _isLocked(){return pending;}
function _lock(){pending=true;}
function _unlock(){pending=false;}
return function(ev){if(preventDefault===true||preventDefault&&preventDefault()){ev.preventDefault();}
if(stopPropagation===true||stopPropagation&&stopPropagation()){ev.stopPropagation();}
if(stopImmediatePropagation===true||stopImmediatePropagation&&stopImmediatePropagation()){ev.stopImmediatePropagation();}
if(_isLocked()){return;}
_lock();const result=fct.apply(this,arguments);Promise.resolve(result).finally(_unlock);return result;};}
__exports.makeButtonHandler=makeButtonHandler;function makeButtonHandler(fct,preventDefault,stopPropagation,stopImmediatePropagation){fct=makeAsyncHandler(fct,preventDefault,stopPropagation,stopImmediatePropagation);return function(ev){const result=fct.apply(this,arguments);const buttonEl=ev.target.closest(BUTTON_HANDLER_SELECTOR);if(!(buttonEl instanceof HTMLElement)){return result;}
buttonEl.classList.add("pe-none");new Promise(resolve=>setTimeout(resolve,DEBOUNCE)).then(()=>{buttonEl.classList.remove("pe-none");const restore=addLoadingEffect(buttonEl);return Promise.resolve(result).then(restore,restore);});return result;};}
return __exports;});;

/* /web/static/src/legacy/js/public/lazyloader.js */
odoo.define('@web/legacy/js/public/lazyloader',['@web/legacy/js/public/minimal_dom'],function(require){'use strict';let __exports={};const{BUTTON_HANDLER_SELECTOR,makeAsyncHandler,makeButtonHandler,}=require('@web/legacy/js/public/minimal_dom');let allScriptsLoadedResolve=null;const _allScriptsLoaded=new Promise(resolve=>{allScriptsLoadedResolve=resolve;}).then(stopWaitingLazy);const retriggeringWaitingProms=[];async function waitForLazyAndRetrigger(ev){const targetEl=ev.target;await _allScriptsLoaded;await Promise.all(retriggeringWaitingProms);setTimeout(()=>{if(targetEl.isConnected){targetEl.dispatchEvent(new ev.constructor(ev.type,ev));}},0);}
const loadingEffectHandlers=[];function registerLoadingEffectHandler(el,type,handler){el.addEventListener(type,handler,{capture:true});loadingEffectHandlers.push({el,type,handler});}
let waitingLazy=false;function waitLazy(){if(waitingLazy){return;}
waitingLazy=true;document.body.classList.add('o_lazy_js_waiting');const mainEl=document.getElementById('wrapwrap')||document.body;const loadingEffectButtonEls=[...mainEl.querySelectorAll(BUTTON_HANDLER_SELECTOR)].filter(el=>{return!el.classList.contains('o_no_wait_lazy_js')&&!(el.nodeName==='A'&&el.href&&el.getAttribute('href')!=='#');});const loadingEffectEventTypes=['mouseover','mouseenter','mousedown','mouseup','click','mouseout','mouseleave'];for(const buttonEl of loadingEffectButtonEls){for(const eventType of loadingEffectEventTypes){const loadingEffectHandler=eventType==='click'?makeButtonHandler(waitForLazyAndRetrigger,true,true,true):makeAsyncHandler(waitForLazyAndRetrigger,true,true,true);registerLoadingEffectHandler(buttonEl,eventType,loadingEffectHandler);}}
for(const formEl of document.querySelectorAll('form:not(.o_no_wait_lazy_js)')){registerLoadingEffectHandler(formEl,'submit',ev=>{ev.preventDefault();ev.stopImmediatePropagation();});}}
function stopWaitingLazy(){if(!waitingLazy){return;}
waitingLazy=false;document.body.classList.remove('o_lazy_js_waiting');for(const{el,type,handler}of loadingEffectHandlers){el.removeEventListener(type,handler,{capture:true});}}
if(document.readyState!=='loading'){waitLazy();}else{document.addEventListener('DOMContentLoaded',function(){waitLazy();});}
if(document.readyState==='complete'){setTimeout(_loadScripts,0);}else{window.addEventListener('load',function(){setTimeout(_loadScripts,0);});}
function _loadScripts(scripts,index){if(scripts===undefined){scripts=document.querySelectorAll('script[data-src]');}
if(index===undefined){index=0;}
if(index>=scripts.length){allScriptsLoadedResolve();return;}
const script=scripts[index];script.addEventListener('load',_loadScripts.bind(this,scripts,index+1));script.setAttribute('defer','defer');script.src=script.dataset.src;script.removeAttribute('data-src');}
__exports[Symbol.for("default")]={loadScripts:_loadScripts,allScriptsLoaded:_allScriptsLoaded,registerPageReadinessDelay:retriggeringWaitingProms.push.bind(retriggeringWaitingProms),};return __exports;});;

/* /web_editor/static/src/js/frontend/loader_loading.js */
(function(){'use strict';document.addEventListener('DOMContentLoaded',()=>{var textareaEls=document.querySelectorAll('textarea.o_wysiwyg_loader');for(var i=0;i<textareaEls.length;i++){var textarea=textareaEls[i];var wrapper=document.createElement('div');wrapper.classList.add('position-relative','o_wysiwyg_textarea_wrapper');var loadingElement=document.createElement('div');loadingElement.classList.add('o_wysiwyg_loading');var loadingIcon=document.createElement('i');loadingIcon.classList.add('text-600','text-center','fa','fa-circle-o-notch','fa-spin','fa-2x');loadingElement.appendChild(loadingIcon);wrapper.appendChild(loadingElement);textarea.parentNode.insertBefore(wrapper,textarea);wrapper.insertBefore(textarea,loadingElement);}});})();;

/* /website/static/src/js/content/inject_dom.js */
odoo.define('@website/js/content/inject_dom',['@web/core/browser/cookie','@web/session'],function(require){'use strict';let __exports={};const{cookie:cookieManager}=require("@web/core/browser/cookie");const{session}=require("@web/session");__exports.unhideConditionalElements=unhideConditionalElements;function unhideConditionalElements(){const styleEl=document.createElement('style');styleEl.id="conditional_visibility";document.head.appendChild(styleEl);const conditionalEls=document.querySelectorAll('[data-visibility="conditional"]');for(const conditionalEl of conditionalEls){const selectors=conditionalEl.dataset.visibilitySelectors;styleEl.sheet.insertRule(`${selectors} { display: none !important; }`);}
for(const conditionalEl of conditionalEls){conditionalEl.classList.remove('o_conditional_hidden');}}
__exports.setUtmsHtmlDataset=setUtmsHtmlDataset;function setUtmsHtmlDataset(){const htmlEl=document.documentElement;const cookieNamesToDataNames={'utm_source':'utmSource','utm_medium':'utmMedium','utm_campaign':'utmCampaign',};for(const[name,dsName]of Object.entries(cookieNamesToDataNames)){const cookie=cookieManager.get(`odoo_${name}`);if(cookie){htmlEl.dataset[dsName]=cookie.replace(/(^["']|["']$)/g,'');}}}
document.addEventListener('DOMContentLoaded',()=>{setUtmsHtmlDataset();const htmlEl=document.documentElement;const country=session.geoip_country_code;if(country){htmlEl.dataset.country=country;}
htmlEl.dataset.logged=!session.is_website_user;unhideConditionalElements();});return __exports;});;

/* /website/static/src/js/content/auto_hide_menu.js */
odoo.define('@website/js/content/auto_hide_menu',[],function(require){'use strict';let __exports={};const BREAKPOINT_SIZES={sm:'575',md:'767',lg:'991',xl:'1199',xxl:'1399'};async function autoHideMenu(el,options){if(!el){return;}
const navbar=el.closest('.navbar');const[breakpoint='md']=navbar?Object.keys(BREAKPOINT_SIZES).filter(suffix=>navbar.classList.contains(`navbar-expand-${suffix}`)):[];const isNoHamburgerMenu=!!navbar&&navbar.classList.contains('navbar-expand');const minSize=BREAKPOINT_SIZES[breakpoint];let isExtraMenuOpen=false;options=Object.assign({unfoldable:'none',images:[],loadingStyleClasses:[],autoClose:()=>true,},options||{});const isUserNavbar=el.parentElement.classList.contains('o_main_navbar');const dropdownSubMenuClasses=['show','border-0','position-static'];const dropdownToggleClasses=['h-auto','py-2','text-secondary'];const autoMarginLeftRegex=/\bm[sx]?(?:-(?:sm|md|lg|xl|xxl))?-auto\b/;const autoMarginRightRegex=/\bm[ex]?(?:-(?:sm|md|lg|xl|xxl))?-auto\b/;var extraItemsToggle=null;const afterFontsloading=new Promise((resolve)=>{if(document.fonts){document.fonts.ready.then(resolve);}else{setTimeout(resolve,150);}});afterFontsloading.then(_adapt);if(options.images.length){await _afterImagesLoading(options.images);_adapt();}
let pending=false;let refreshId=null;const onRefresh=()=>{if(pending){refreshId=window.requestAnimationFrame(onRefresh);_adapt();pending=false;}else{refreshId=null;}};const throttleAdapt=()=>{if(refreshId===null){refreshId=window.requestAnimationFrame(onRefresh);_adapt();}else{pending=true;}};window.addEventListener('resize',throttleAdapt);function _restore(){if(!extraItemsToggle){return;}
[...extraItemsToggle.querySelector('.dropdown-menu').children].forEach((item)=>{if(!isUserNavbar){item.classList.add('nav-item');const itemLink=item.querySelector('.dropdown-item');if(itemLink){itemLink.classList.remove('dropdown-item');itemLink.classList.add('nav-link');}}else{item.classList.remove('dropdown-item');const dropdownSubMenu=item.querySelector('.dropdown-menu');const dropdownSubMenuButton=item.querySelector('.dropdown-toggle');if(dropdownSubMenu){dropdownSubMenu.classList.remove(...dropdownSubMenuClasses);}
if(dropdownSubMenuButton){dropdownSubMenuButton.classList.remove(...dropdownToggleClasses);}}
el.insertBefore(item,extraItemsToggle);});extraItemsToggle.remove();extraItemsToggle=null;}
function _adapt(){const wysiwyg=window.$&&$('#wrapwrap').data('wysiwyg');const odooEditor=wysiwyg&&wysiwyg.odooEditor;if(odooEditor){odooEditor.observerUnactive("adapt");odooEditor.withoutRollback(__adapt);odooEditor.observerActive("adapt");return;}
__adapt();}
function __adapt(){if(options.loadingStyleClasses.length){el.classList.add(...options.loadingStyleClasses);}
const extraMenuEl=_getExtraMenuEl();isExtraMenuOpen=extraMenuEl&&extraMenuEl.classList.contains("show");_restore();if(!el.getClientRects().length||el.closest('.show')||(window.matchMedia(`(max-width: ${minSize}px)`).matches&&!isNoHamburgerMenu)){return _endAutoMoreMenu();}
let unfoldableItems=[];const items=[...el.children].filter((node)=>{if(node.matches&&!node.matches(options.unfoldable)){return true;}
unfoldableItems.push(node);return false;});var nbItems=items.length;var menuItemsWidth=items.reduce((sum,el)=>sum+computeFloatOuterWidthWithMargins(el,true,true,false),0);let maxWidth=0;if(!maxWidth){maxWidth=computeFloatOuterWidthWithMargins(el,true,true,true);var style=window.getComputedStyle(el);maxWidth-=(parseFloat(style.paddingLeft)+parseFloat(style.paddingRight)+parseFloat(style.borderLeftWidth)+parseFloat(style.borderRightWidth));maxWidth-=unfoldableItems.reduce((sum,el)=>sum+computeFloatOuterWidthWithMargins(el,true,true,false),0);}
if(maxWidth-menuItemsWidth>=-0.001){return _endAutoMoreMenu();}
const dropdownMenu=_addExtraItemsButton(items[nbItems-1].nextElementSibling);menuItemsWidth+=computeFloatOuterWidthWithMargins(extraItemsToggle,true,true,false);do{menuItemsWidth-=computeFloatOuterWidthWithMargins(items[--nbItems],true,true,false);}while(!(maxWidth-menuItemsWidth>=-0.001)&&(nbItems>0));const extraItems=items.slice(nbItems);extraItems.forEach((el)=>{if(!isUserNavbar){const navLink=el.querySelector('.nav-link, a');el.classList.remove('nav-item');if(navLink){navLink.classList.remove('nav-link');navLink.classList.add('dropdown-item');navLink.classList.toggle('active',el.classList.contains('active'));}}else{const dropdownSubMenu=el.querySelector('.dropdown-menu');const dropdownSubMenuButton=el.querySelector('.dropdown-toggle');el.classList.add('dropdown-item','p-0');if(dropdownSubMenu){dropdownSubMenu.classList.add(...dropdownSubMenuClasses);}
if(dropdownSubMenuButton){dropdownSubMenuButton.classList.add(...dropdownToggleClasses);}}
dropdownMenu.appendChild(el);});_endAutoMoreMenu();}
function computeFloatOuterWidthWithMargins(el,mLeft,mRight,considerAutoMargins){var rect=el.getBoundingClientRect();var style=window.getComputedStyle(el);var outerWidth=rect.right-rect.left;const isRTL=style.direction==='rtl';if(mLeft!==false&&(considerAutoMargins||!(isRTL?autoMarginRightRegex:autoMarginLeftRegex).test(el.getAttribute('class')))){outerWidth+=parseFloat(style.marginLeft);}
if(mRight!==false&&(considerAutoMargins||!(isRTL?autoMarginLeftRegex:autoMarginRightRegex).test(el.getAttribute('class')))){outerWidth+=parseFloat(style.marginRight);}
return isNaN(outerWidth)?0:outerWidth;}
function _addExtraItemsButton(target){let dropdownMenu=document.createElement('div');extraItemsToggle=dropdownMenu.cloneNode();const extraItemsToggleIcon=document.createElement('i');const extraItemsToggleLink=document.createElement('a');dropdownMenu.className='dropdown-menu';extraItemsToggle.className='nav-item dropdown o_extra_menu_items';extraItemsToggle.setAttribute("role","presentation");extraItemsToggleIcon.className='fa fa-plus';const extraItemsToggleAriaLabel=el.closest("[data-extra-items-toggle-aria-label]")?.dataset.extraItemsToggleAriaLabel;Object.entries({role:'menuitem',href:'#',class:'nav-link dropdown-toggle o-no-caret','data-bs-toggle':'dropdown','aria-expanded':false,'aria-label':extraItemsToggleAriaLabel||" ",}).forEach(([key,value])=>{extraItemsToggleLink.setAttribute(key,value);});extraItemsToggleLink.appendChild(extraItemsToggleIcon);extraItemsToggle.appendChild(extraItemsToggleLink);extraItemsToggle.appendChild(dropdownMenu);el.insertBefore(extraItemsToggle,target);if(!options.autoClose()){extraItemsToggleLink.setAttribute("data-bs-auto-close","outside");}
return dropdownMenu;}
function _afterImagesLoading(images){const defs=images.map((image)=>{if(image.complete||!image.getClientRects().length){return null;}
return new Promise(function(resolve,reject){if(!image.width){image.classList.add('o_menu_image_placeholder');}
image.addEventListener('load',()=>{image.classList.remove('o_menu_image_placeholder');resolve();});});});return Promise.all(defs);}
function _getExtraMenuEl(){return el.querySelector(".o_extra_menu_items .dropdown-toggle");}
function _endAutoMoreMenu(){const extraMenuEl=_getExtraMenuEl();if(extraMenuEl&&isExtraMenuOpen){extraMenuEl.click();}
el.classList.remove(...options.loadingStyleClasses);}}
document.addEventListener('DOMContentLoaded',async()=>{const header=document.querySelector('header#top');if(header){const topMenu=header.querySelector(".top_menu");const unfoldable=".divider, .divider ~ li, .o_no_autohide_item, .js_language_selector";if(!topMenu.querySelector(`:scope > :not(${unfoldable})`)||header.classList.contains("o_no_autohide_menu")){topMenu.classList.remove('o_menu_loading');return;}
const excludedImagesSelector='.o_mega_menu, .o_offcanvas_logo_container, .o_lang_flag';const excludedImages=[...header.querySelectorAll(excludedImagesSelector)];const images=[...header.querySelectorAll('img')].filter((img)=>{excludedImages.forEach(node=>{if(node.contains(img)){return false;}});return img.matches&&!img.matches(excludedImagesSelector);});autoHideMenu(topMenu,{unfoldable:unfoldable,images:images,loadingStyleClasses:['o_menu_loading'],autoClose:()=>!document.body.classList.contains("editor_enable"),});}});return __exports;});;

/* /website/static/src/js/content/redirect.js */
odoo.define('@website/js/content/redirect',['@web/session'],function(require){'use strict';let __exports={};const{session}=require('@web/session');document.addEventListener('DOMContentLoaded',()=>{if(session.is_website_user){return;}
if(!window.frameElement){const frontendToBackendNavEl=document.querySelector('.o_frontend_to_backend_nav');if(frontendToBackendNavEl){frontendToBackendNavEl.classList.add('d-flex');frontendToBackendNavEl.classList.remove('d-none');}
const currentUrl=new URL(window.location.href);currentUrl.pathname=`/@${currentUrl.pathname}`;if(currentUrl.searchParams.get('enable_editor')||currentUrl.searchParams.get('edit_translations')){document.body.innerHTML='';window.location.replace(currentUrl.href);return;}
const backendEditBtnEl=document.querySelector('.o_frontend_to_backend_edit_btn');if(backendEditBtnEl){backendEditBtnEl.href=currentUrl.href;document.addEventListener("keydown",ev=>{if(ev.key==="a"&&ev.altKey){currentUrl.searchParams.set('enable_editor',1);window.location.replace(currentUrl.href);}},true);}}else{const backendUserDropdownLinkEl=document.getElementById('o_backend_user_dropdown_link');if(backendUserDropdownLinkEl){backendUserDropdownLinkEl.classList.add('d-none');backendUserDropdownLinkEl.classList.remove('d-flex');}
window.frameElement.dispatchEvent(new CustomEvent('OdooFrameContentLoaded'));}});return __exports;});;

/* /website/static/src/js/content/adapt_content.js */
odoo.define('@website/js/content/adapt_content',[],function(require){'use strict';let __exports={};document.addEventListener('DOMContentLoaded',()=>{const htmlEl=document.documentElement;const editTranslations=!!htmlEl.dataset.edit_translations;if(editTranslations){[...document.querySelectorAll('textarea')].map(textarea=>{if(textarea.value.indexOf('data-oe-translation-source-sha')!==-1){textarea.classList.add('o_text_content_invisible');}});}
const searchModalEl=document.querySelector("header#top .modal#o_search_modal");if(searchModalEl){const mainEl=document.querySelector("main");const searchDivEl=document.createElement('div');searchDivEl.id="o_search_modal_block";searchDivEl.appendChild(searchModalEl);mainEl.appendChild(searchDivEl);}});return __exports;});
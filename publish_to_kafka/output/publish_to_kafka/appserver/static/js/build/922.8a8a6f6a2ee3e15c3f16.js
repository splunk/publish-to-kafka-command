(self.webpackChunk_splunk_ucc_ui_lib=self.webpackChunk_splunk_ucc_ui_lib||[]).push([[922],{8351:(e,t,n)=>{(()=>{"use strict";var t={n:e=>{var n=e&&e.__esModule?()=>e.default:()=>e;return t.d(n,{a:n}),n},d:(e,n)=>{for(var r in n)t.o(n,r)&&!t.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:n[r]})},o:(e,t)=>Object.prototype.hasOwnProperty.call(e,t),r:e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}},r={};t.r(r),t.d(r,{default:()=>p});const a=n(7294);var o=t.n(a);const l=n(6817);var i=t.n(l);const u=n(7021);var c=new Map;c.set("outlined",(function(){return o().createElement(o().Fragment,null,o().createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M8.94008 2C8.11165 2 7.44008 2.67157 7.44008 3.5V9H5.47861C4.11314 9 3.45783 10.676 4.46119 11.6022L10.9824 17.6218C11.557 18.1521 12.4426 18.1521 13.0172 17.6217L19.5384 11.6022C20.5417 10.676 19.8864 9 18.5209 9H16.5553V3.5C16.5553 2.67157 15.8838 2 15.0553 2H8.94008ZM9.44008 11V4H14.5553V11H17.2421L11.9998 15.8391L6.75743 11H9.44008Z"}),o().createElement("path",{d:"M4 20C3.44772 20 3 20.4477 3 21C3 21.5523 3.44772 22 4 22H20C20.5523 22 21 21.5523 21 21C21 20.4477 20.5523 20 20 20H4Z"}))})),c.set("filled",(function(){return o().createElement(o().Fragment,null,o().createElement("path",{d:"M7.44032 3.5C7.44032 2.67157 8.1119 2 8.94032 2H15.0556C15.884 2 16.5556 2.67157 16.5556 3.5V9H18.5212C19.8867 9 20.542 10.676 19.5386 11.6022L13.0174 17.6217C12.4429 18.1521 11.5572 18.1521 10.9826 17.6218L4.46143 11.6022C3.45808 10.676 4.11338 9 5.47885 9H7.44032V3.5Z"}),o().createElement("path",{d:"M3 21C3 20.4477 3.44772 20 4 20H20C20.5523 20 21 20.4477 21 21C21 21.5523 20.5523 22 20 22H4C3.44772 22 3 21.5523 3 21Z"}))}));var f=["default","outlined","filled"],s=function(e){return"default"===e||e&&!function(e){return f.indexOf(e)>=0}(e)?"outlined":e},m=function(e){var t=e.children,n=e.variant,r=function(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}(e,["children","variant"]),l=s(n),f="arrowbroadunderbardown-".concat(l),m=(0,a.useContext)(u.IconContext),p=c.get(l);if(m&&p){var d=m.toRender;if((0,m.addIcon)(f,p()),!d)return null}return o().createElement(i(),r,t,m?o().createElement("use",{href:"#".concat(f)}):!!p&&p())};m.defaultProps={variant:"default"};const p=m;e.exports=r})()},5922:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>oe});var r=n(7294),a=n(6219),o=n(2672),l=n.n(o),i=n(1946),u=n.n(i),c=n(1569),f=n.n(c),s=n(2788),m=n(6622),p=n(4695),d=n(2681),b=n(775),y=n(5697),v=n.n(y),g=n(7123);function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function O(e){var t,n,o=e.tab,l=(t=(0,r.useState)(!0),n=2,function(e){if(Array.isArray(e))return e}(t)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,o,l,i=[],u=!0,c=!1;try{if(o=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;u=!1}else for(;!(u=(r=o.call(n)).done)&&(i.push(r.value),i.length!==t);u=!0);}catch(e){c=!0,a=e}finally{try{if(!u&&null!=n.return&&(l=n.return(),Object(l)!==l))return}finally{if(c)throw a}}return i}}(t,n)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?h(e,t):void 0}}(t,n)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()),i=l[0],u=l[1],c=(0,r.useRef)(null),f=(0,p.YK)().meta.name;return(0,r.useEffect)((function(){new Promise((function(e){"external"===o.customTab.type?import("".concat((0,g.a)(),"/custom/").concat(o.customTab.src,".js")).then((function(t){var n=t.default;e(n)})):require(["app/".concat(f,"/js/build/custom/").concat(o.customTab.src)],(function(t){return e(t)}))})).then((function(e){new e(o,c.current).render(),u(!1)}))}),[]),r.createElement(r.Fragment,null,i&&(0,a._)("Loading..."),r.createElement("div",{ref:c,style:{visibility:i?"hidden":"visible"}}))}O.propTypes={tab:v().object.isRequired};const E=O;var j,S=n(5414),w=n.n(S),C=n(1181),A=n(2054),P=n(9643),I=n(6188),T=n(457),k=n(3433);function x(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,o,l,i=[],u=!0,c=!1;try{if(o=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;u=!1}else for(;!(u=(r=o.call(n)).done)&&(i.push(r.value),i.length!==t);u=!0);}catch(e){c=!0,a=e}finally{try{if(!u&&null!=n.return&&(l=n.return(),Object(l)!==l))return}finally{if(c)throw a}}return i}}(e,t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?_(e,t):void 0}}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var L,N,M=s.default.div(j||(L=["\n    margin-left: 270px !important;\n    width: 150px;\n"],N||(N=L.slice(0)),j=Object.freeze(Object.defineProperties(L,{raw:{value:Object.freeze(N)}}))));function H(e){var t=e.serviceName,n=(0,r.useRef)(),o=x((0,r.useState)(null),2),l=o[0],i=o[1],u=x((0,r.useState)(!1),2),c=u[0],f=u[1],s=x((0,r.useState)({}),2),m=s[0],p=s[1];if((0,r.useEffect)((function(){(0,P.L)({serviceName:"settings/".concat(t),handleError:!0,callbackOnError:function(e){e.uccErrorCode="ERR0005",i(e)}}).then((function(e){p(e.data.entry[0].content)}))}),[t]),null!=l&&l.uccErrorCode)throw l;return Object.keys(m).length?r.createElement(r.Fragment,null,r.createElement(C.Z,{ref:n,page:k.y,stanzaName:t,serviceName:"settings",mode:I.DE,currentServiceState:m,handleFormSubmit:function(e){f(e)}}),r.createElement(M,null,r.createElement(A.Sn,{className:"saveBtn",appearance:"primary",label:c?r.createElement(w(),null):(0,a._)("Save"),onClick:function(){n.current.handleSubmit()},disabled:c}))):r.createElement(T.XE,{size:"medium"})}H.propTypes={serviceName:v().string.isRequired};const R=H;var Z=n(7120),z=n(6516),D=n(5354),U=n(9190),q=n(3985);function V(e){return V="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},V(e)}function F(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function $(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?F(Object(n),!0).forEach((function(t){var r,a,o;r=e,a=t,o=n[t],(a=function(e){var t=function(e,t){if("object"!==V(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,"string");if("object"!==V(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return String(e)}(e);return"symbol"===V(t)?t:String(t)}(a))in r?Object.defineProperty(r,a,{value:o,enumerable:!0,configurable:!0,writable:!0}):r[a]=o})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):F(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function B(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function K(e){var t,n,a=e.selectedTab,o=e.updateIsPageOpen,l=(t=(0,r.useState)({open:!1}),n=2,function(e){if(Array.isArray(e))return e}(t)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,o,l,i=[],u=!0,c=!1;try{if(o=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;u=!1}else for(;!(u=(r=o.call(n)).done)&&(i.push(r.value),i.length!==t);u=!0);}catch(e){c=!0,a=e}finally{try{if(!u&&null!=n.return&&(l=n.return(),Object(l)!==l))return}finally{if(c)throw a}}return i}}(t,n)||function(e,t){if(e){if("string"==typeof e)return B(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?B(e,t):void 0}}(t,n)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()),i=l[0],u=l[1],c=a.style===q.G;(0,r.useEffect)((function(){c&&o(!!i.open)}),[i]);return r.createElement(Z.W,{value:null},c&&i.open&&r.createElement(U.Z,{open:i.open,handleRequestClose:function(){u($($({},i),{},{open:!1}))},serviceName:a.name,stanzaName:i.stanzaName,mode:i.mode,formLabel:i.formLabel,page:k.y}),r.createElement("div",{style:c&&i.open?{display:"none"}:{display:"block"}},r.createElement(z.Z,{page:k.y,serviceName:a.name,handleRequestModalOpen:function(){u($($({},i),{},{open:!0,mode:I.jg,formLabel:"Add ".concat(a.title)}))},handleOpenPageStyleDialog:function(e,t){u($($({},i),{},{open:!0,stanzaName:e.name,formLabel:t===I.Oh?"Clone ".concat(a.title):"Update ".concat(a.title),mode:t}))}})),!c&&i.open&&r.createElement(D.Z,{page:k.y,open:i.open,handleRequestClose:function(){u($($({},i),{},{open:!1}))},serviceName:a.name,mode:I.jg,formLabel:i.formLabel}))}K.propTypes={selectedTab:v().object,updateIsPageOpen:v().func};const Y=(0,r.memo)(K);var G=n(8351),W=n.n(G),X=n(6416),J=n.n(X);const Q=function(e){return r.createElement(J(),{target:"_blank",to:e.fileUrl,download:e.fileNameAfterDownload,"data-test":"downloadButton"},e.children)},ee=function(){return r.createElement("div",null,r.createElement(Q,{fileUrl:(0,g.a)().replace("js/build","openapi.json"),fileNameAfterDownload:"openapi.json"},r.createElement(W(),null),r.createElement("span",null,"OpenAPI.json")))};var te;function ne(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,o,l,i=[],u=!0,c=!1;try{if(o=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;u=!1}else for(;!(u=(r=o.call(n)).done)&&(i.push(r.value),i.length!==t);u=!0);}catch(e){c=!0,a=e}finally{try{if(!u&&null!=n.return&&(l=n.return(),Object(l)!==l))return}finally{if(c)throw a}}return i}}(e,t)||function(e,t){if(e){if("string"==typeof e)return re(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?re(e,t):void 0}}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function re(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var ae=(0,s.default)(f().Row)(te||(te=function(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(["\n    padding: 5px 0px;\n\n    .dropdown {\n        text-align: right;\n    }\n\n    .input_button {\n        text-align: right;\n        margin-right: 0px;\n    }\n"])));const oe=function(){var e=(0,p.YK)().pages.configuration,t=e.title,n=e.description,o=e.tabs,i=o.map((function(e){return e.name})),c=ne((0,r.useState)(o[0].name),2),s=c[0],y=c[1],v=ne((0,r.useState)(!1),2),g=v[0],h=v[1],O=(0,m.Z)();(0,r.useEffect)((function(){O&&i.includes(O.get("tab"))&&O.get("tab")!==s&&y(O.get("tab"))}),[]);var j=(0,r.useCallback)((function(e,t){var n=t.selectedTabId;y(n),h(!1)}),[s]),S=function(e){h(e)};return r.createElement(b.Z,null,r.createElement("div",{style:g?{display:"none"}:{display:"block"}},r.createElement(f(),{gutter:8},r.createElement(ae,null,r.createElement(f().Column,{span:9},r.createElement(d.r3,null,(0,a._)(t)),r.createElement(d.pZ,null,(0,a._)(n||""))),r.createElement(f().Column,{span:1,style:{textAlignLast:"right"}},r.createElement(ee,null)))),r.createElement(l(),{activeTabId:s,onChange:j},o.map((function(e){return r.createElement(l().Tab,{key:e.name,label:(0,a._)(e.title),tabId:e.name})})))),o.map((function(e){return function(e){var t;return t=null!=e&&e.customTab?function(e){return r.createElement(E,{tab:e})}(e):null!=e&&e.table?r.createElement(Y,{key:e.name,selectedTab:e,updateIsPageOpen:S}):r.createElement(R,{key:e.name,serviceName:e.name}),r.createElement("div",{key:e.name,style:e.name!==s?{display:"none"}:{display:"block"},id:"".concat(e.name,"Tab")},t)}(e)})),r.createElement(u(),{position:"top-right"}))}}}]);
//# sourceMappingURL=922.8a8a6f6a2ee3e15c3f16.js.map
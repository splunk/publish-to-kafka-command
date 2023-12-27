// Derived from: https://splunk.github.io/addonfactory-ucc-generator/custom_ui_extensions/custom_hook/
class ConfigEnvHook {
    /**
     * Form hook
     * @constructor
     * @param {Object} globalConfig - Global configuration.
     * @param {string} serviceName - Service name
     * @param {object} state - object with state of the components on the servcice/page
     * @param {string} mode - edit,create or clone
     * @param {object} util - the utility object
     */
    constructor(globalConfig, serviceName, state, mode, util, groupName) {
        this.globalConfig = globalConfig;
        this.serviceName = serviceName;
        this.state = state;
        this.mode = mode;
        this.util = util;
        this.groupName = groupName;
        console.log('Inside Hook mode: ', mode);
    }

    updateDisplayAuthFields(shouldShow) {
        this.util.setState((prevState) => {
            let data = {...prevState.data};
            data.sasl_plain_username.display = shouldShow;
            data.sasl_plain_password.display = shouldShow;
            return {data};
        });
    }

    onCreate() {
        if (this.mode === "create") {
            console.log('in Hook: onCreate');
            const show_auth_fields = this.state.data.security_protocol.value !== 'PLAINTEXT'
            this.updateDisplayAuthFields(show_auth_fields);
        }
    }


    onChange(field, value, dataDict) {
        // console.log('in Hook: onChange ', field, ' value : ', value);
        if (field === 'security_protocol') {
            this.updateDisplayAuthFields(value !== 'PLAINTEXT');
        }
    }

    onRender() {
        console.log('in Hook: onRender');
    }

    /*
        Put form validation logic here.
        Return ture if validation pass, false otherwise.
        Call displayErrorMsg when validtion failed.
    */
    onSave(dataDict) {
        // console.log('in Hook: onSave with data: ', dataDict);
        if(dataDict.security_protocol === 'SASL_PLAINTEXT'){
            if(dataDict.sasl_plain_username === '' || dataDict.sasl_plain_password === ''){
                this.util.setErrorMsg('Username and Password are required when security protocol is SASL_PLAINTEXT');
                return false;
            }
        }
        return true;
    }

    onSaveSuccess() {
        console.log('in Hook: onSaveSuccess');
    }

    onSaveFail() {
        console.log('in Hook: onSaveFail');
    }

    /*
    Put logic here to execute javascript after loading edit UI.
    */
    onEditLoad() {
        console.log('in Hook: onEditLoad');
    }
}

export default ConfigEnvHook;
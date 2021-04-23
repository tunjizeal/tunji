import alertify from 'alertifyjs';
import { KEY_CODES } from 'js/constants';

/**
 * @namespace MultiButton
 * @param {string} label
 * @param {function} callback
 */

/**
 * Use this custom alertify modal to display multiple buttons with different
 * callbacks.
 *
 * @param {string} confirmId needs to be unique
 * @param {string} [title] optional
 * @param {string} [message] optional
 * @param {MultiButton[]} buttons
 */
export function multiConfirm(confirmId, title, message, buttons) {
  // `confirmId` needs to be uniqe, as alertify requires the custom dialog to be
  // defined before it is being invoked.
  // We check if it haven't been already defined to avoid errors and unnecessary
  // calls.
  if (!alertify[confirmId]) {
    // define new alertify dialog
    alertify.dialog(
      confirmId,
      function() {
        return {
          setup: function() {
            const buttonsArray = [];
            buttons.forEach((button, i) => {
              buttonsArray.push({
                text: button.label,
                className: alertify.defaults.theme.ok,
                scope: 'primary',
                element: undefined,
                index: i,
              });
            });
            return {
              buttons: buttonsArray,
              options: {
                title: title,
                basic: false,
                movable: false,
                resizable: false,
                closable: true,
                maximizable: false,
                pinnable: false,
              },
            };
          },
          prepare: function() {
            if (message) {
              this.setContent(message);
            }
          },
          settings: {
            onclick: null,
          },
          callback: function(closeEvent) {
            this.settings.onclick(closeEvent);
          },
        };
      },
      false,
      'confirm'
    );
  }

  const dialog = alertify[confirmId]();

  // set up closing modal on ESC key
  const killMe = (evt) => {
    if (evt.keyCode === KEY_CODES.ESC) {
      dialog.destroy();
    }
  };

  dialog
    .set({
      onclick: (closeEvent) => {
        // button click operates on the button array indexes to know which
        // callback needs to be triggered
        if (buttons[closeEvent.index] && buttons[closeEvent.index].callback) {
          buttons[closeEvent.index].callback();
        }
      },
      onshow: () => {
        $(document).on('keyup', killMe);
      },
      onclose: () => {
        $(document).off('keyup', killMe);
      },
    })
    .show();
}
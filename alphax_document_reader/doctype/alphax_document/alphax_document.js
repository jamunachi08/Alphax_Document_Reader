frappe.ui.form.on('AlphaX Document', {
  refresh(frm) {
    frm.add_custom_button(__('Extract Text'), () => {
      frm.call('extract_text')
        .then(() => frm.reload_doc())
        .catch(() => {});
    }).addClass('btn-primary');
  }
});

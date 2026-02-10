frappe.pages['document-reader'].on_page_load = function(wrapper) {
  const page = frappe.ui.make_app_page({
    parent: wrapper,
    title: 'AlphaX Document Reader',
    single_column: true
  });

  $(wrapper).find('.layout-main-section').html(`
    <div class="axdr-wrap">
      <div class="axdr-card">
        <div><b>Extract Text</b></div>
        <div class="axdr-muted">Pick any file from File doctype (public/private) and extract plain text.</div>
        <hr>
        <div class="form-group">
          <label>File URL</label>
          <input type="text" class="form-control" id="axdr_file_url" placeholder="/files/sample.pdf">
        </div>
        <div class="checkbox">
          <label><input type="checkbox" id="axdr_force_ocr"> Force OCR (if available)</label>
        </div>
        <button class="btn btn-primary" id="axdr_run">Extract</button>
      </div>

      <div class="axdr-card">
        <div><b>Output</b></div>
        <pre id="axdr_out" style="white-space:pre-wrap; min-height:180px;"></pre>
      </div>
    </div>
  `);

  $('#axdr_run').on('click', () => {
    const file_url = $('#axdr_file_url').val();
    const force_ocr = $('#axdr_force_ocr').is(':checked') ? 1 : 0;

    if (!file_url) {
      frappe.msgprint('File URL is required');
      return;
    }

    $('#axdr_out').text('Working...');
    frappe.call({
      method: 'alphax_document_reader.api.extract_text',
      args: { file_url, force_ocr },
      callback: (r) => {
        const msg = r.message || {};
        $('#axdr_out').text(msg.text || '');
      },
      error: () => $('#axdr_out').text('Error (check console / server error log)')
    });
  });
};

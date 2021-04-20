$(function (){

	const Editor = toastui.Editor;

	console.log('initial value', $('#body').val());

	const editor = new Editor({
	  el: document.querySelector('#editor'),
	  height: '500px',
	  initialEditType: 'wysiwyg',
	  previewStyle: 'vertical',
	  initialValue: $('#body').val()
	});

	$('.submit-button').on('click', function(evt){
		evt.preventDefault();
		//console.log(editor)
		//alert('submitting' + editor.getMarkdown());

		$('#body').val(editor.getMarkdown());
		$('#post-form').submit();

	})

});
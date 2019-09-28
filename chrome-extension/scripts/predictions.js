$(document).ready(function() {
	startVue();
});

function startVue() {
    Vue.use(Buefy);
	var app = new Vue({
	    el: '#app',
        data: {
	        message: "1231231",
            isLoading: false,
        },
        created() {
	        this.isLoading = true;
	        chrome.storage.sync.get("requestInfo", res => {
				let data = res.requestInfo;
  			    $.post('http://127.0.0.1:5000/build', JSON.stringify(data))
                    .done( (response) => {
                        console.log(`cool`, response);
                        this.isLoading = false;
                    });
				console.log(data)
			});

        },
	});
}
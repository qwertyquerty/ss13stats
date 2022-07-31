function construct_chart(canvas_id, title, endpoint, label_map, data_map, refresh_rate = 600) {
	let chart_options = {
		type: 'line',
		data: {
			labels: [],
			datasets: [{
				label: title,
				data: [],
				borderColor: "#00ff00aa",
				trendlineLinear: {
					style: "#ff0000aa",
					lineStyle: "dotted",
					width: 2
				}
			}]
		},
		options: {
			responsive: true,
			scales: {
				x: {
					ticks: {
						display: false
					}
			   }
			}
		}
	}

	const chart = new Chart(document.getElementById(canvas_id), chart_options)

	function update_chart() {
		$.getJSON(endpoint, function(data) {
			chart.data.labels = data.map(label_map)
			chart.data.datasets[0].data = data.map(data_map)

			chart.update()
		})
	}

	update_chart();

	setInterval(update_chart, refresh_rate * 1000)
}
async function initChart() {
    const res = await fetch("/statistics/tags/")
    const dataRes = await res.json()

    console.log(dataRes)

    const { tags, statistics } = dataRes

    const labels = tags.map((tag) => tag.name)
    const data = tags.map((tag) => tag.ref_count)

    const ctx = document.getElementById("chart-tags").getContext("2d")
    const myChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels,
            datasets: [{
                label: "Count references",
                data,
                hoverOffset: 4
            }]
        }
    })
}

initChart()

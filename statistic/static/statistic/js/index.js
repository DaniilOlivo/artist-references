function updateStatsTag(tag) {
    const title = document.querySelector("#title-active-tag")
    title.textContent = tag.name

    const statsBlocks = document.querySelectorAll(".statistics-block_tag")
    for (const block of statsBlocks) {
        if (Number(block.dataset.id) === tag.id) {
            block.classList.add("statistics-block_tag_active")
        } else {
            block.classList.remove("statistics-block_tag_active")
        }
    }
}

async function initChart() {
    const res = await fetch("/statistics/tags/")
    const tags = await res.json()

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
        },
        options: {
            onClick: (e) => {
                const res = myChart.getElementsAtEventForMode(
                    e,
                    'nearest',
                    { intersect: true },
                    true
                )
                
                if (res.length === 0) return

                const label = myChart.data.labels[res[0].index]
                const result = tags.find((tag) => tag.name === label)

                if (!result) return
                updateStatsTag(result)
            }
        }
    })

    updateStatsTag(tags[0])
}

initChart()

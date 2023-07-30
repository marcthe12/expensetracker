/**
 * Category type in Javascript
 * @typedef {Object} Category 
 * @property {Number} id 
 * @property {string} name 
 */

/**
 * Expense Type needed for summary 
 * @typedef {Object} Expense
 * @property {Category} category 
 * @property {Number} amount 
 */

/***
 * The main function
 */
async function main() {
    const data = await getData()
    const root = document.getElementById("root")
    // Extract Labels
    const labels = uniq(data.map(
        ({ category }) => category),
        ({ id }) => id
    ).sort((a, b) => a.id - b.id)
    createGraphs(root, data, labels)
    generateTable(root, data, labels)
}

/**
 * Crete the Table 
 * @param {HTMLElement} root 
 * @param {Expense[]} data 
 * @param {str[]} labels 
 */
function generateTable(root, data, labels) {
    const summary = group_cat(data, labels)

    const table = document.createElement("table")
    table.style.margin = "1rem auto"
    root.append(table)

    table.createTHead()
    table.createTFoot()

    const row = table.tHead.insertRow()
    row.append(...["Category", "Amount"].map(element => {
        const header = document.createElement("th")
        header.append(element)
        return header
    }))

    summary.forEach(element => {
        const row = table.insertRow()

        const link = document.createElement("a")
        row.insertCell().append(link)
        link.href = `/cat/${element.category.id}`
        link.append(element.category.name)

        row.insertCell().append(element.amount.toFixed(2))
    })

    const footer = table.tFoot.insertRow();
    [
        "Overall",
        summary.reduce((partialSum, { amount }) => partialSum + amount, 0).toFixed(2)
    ].forEach(element => {
        footer.insertCell().append(element)
    })
}

/**
 * Create The Pie Charts 
 * @param {HTMLElement} root 
 * @param {Expense[]} data 
 * @param {str[]} labels 
 */
function createGraphs(root, data, labels) {
    const graphBar = document.createElement("div")
    root.append(graphBar)
    graphBar.style.display = "grid"
    graphBar.style.gridAutoFlow = "column"
    pieChart(graphBar, group_cat(data.filter(({ amount }) => amount < 0), labels), "Outflow")
    pieChart(graphBar, group_cat(data.filter(({ amount }) => amount > 0), labels), "Inflow")
}

/**
 * Fetches the summary Data
 * @returns {Promise<Expense[]>}
 */
async function getData() {
    const res = await fetch("/summary.json")
    const raw = await res.json()

    const data = raw.map(({ amount, category }) => ({ amount, category }))
    return data
}

/**
 * Group the data by category
 * @param {Expense[]} data 
 * @param {Category[]} labels 
 * @returns {Expense[]}
 */
function group_cat(data, labels = []) {
    return data.reduce((accumulator, { category, amount }) => {
        const index = accumulator.find(element => element.category.id == category.id)
        if (index !== undefined) {
            index.amount += amount
            return accumulator
        } else {
            return [...accumulator, { category, amount }]
        }
    }, labels.map(category => ({ category, amount: 0 })))
}

/**
 * Create a pie chart from the data
 * @param {element} root 
 * @param {any[]} data 
 * @param {str} title 
 */
function pieChart(root, data, title = "") {
    const ctx = document.createElement('canvas')

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: data.map(({ category }) => category.name),
            datasets: [{
                data: data.map(({ amount }) => amount)
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: title
                }
            }
        }
    })
    root.append(ctx)
}

/**
 * get the unique value in an array
 * @param {any[]} arr 
 * @param {(any) => any} key 
 * @returns any[]
 */
function uniq(arr, key) {
    var seen = new Set()
    return arr.filter((item) => {
        var k = key(item)
        return seen.has(k) ? false : seen.add(k)
    })
}


window.onload = main
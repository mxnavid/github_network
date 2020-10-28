function autoBox() {
    document.body.appendChild(this);
    const {x, y, width, height} = this.getBBox();
    document.body.removeChild(this);
    return [x, y, width, height];
}

function tree(data) {
    const root = d3.hierarchy(data).sort((a, b) => d3.descending(a.height, b.height) || d3.ascending(a.data.name, b.data.name));
    root.dx = 10;
    root.dy = window.width / (root.height + 1);
    return d3.cluster().nodeSize([root.dx, root.dy])(root);
}

function chart(data) {
    const root = tree(data);

  const svg = d3.create("svg");

  svg.append("g")
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-opacity", 0.4)
    .attr("stroke-width", 1.5)
  .selectAll("path")
    .data(root.links())
    .join("path")
      .attr("d", d => `
        M${d.target.y},${d.target.x}
        C${d.source.y + root.dy / 2},${d.target.x}
         ${d.source.y + root.dy / 2},${d.source.x}
         ${d.source.y},${d.source.x}
      `);

  svg.append("g")
    .selectAll("circle")
    .data(root.descendants())
    .join("circle")
      .attr("cx", d => d.y)
      .attr("cy", d => d.x)
      .attr("fill", d => d.children ? "#555" : "#999")
      .attr("r", 2.5);

  svg.append("g")
      .attr("font-family", "sans-serif")
      .attr("font-size", 10)
      .attr("stroke-linejoin", "round")
      .attr("stroke-width", 3)
    .selectAll("text")
    .data(root.descendants())
    .join("text")
      .attr("x", d => d.y)
      .attr("y", d => d.x)
      .attr("dy", "0.31em")
      .attr("dx", d => d.children ? -6 : 6)
      .text(d => d.data.name)
    .filter(d => d.children)
      .attr("text-anchor", "end")
    .clone(true).lower()
      .attr("stroke", "white");

  return svg.attr("viewBox", autoBox).node();
}

document.addEventListener('DOMContentLoaded', (ev) => {
    d3.json('/repos').then(data => {
        window.width = 2000;
        var s = chart(data);
        console.log(s);
        document.body.append(s);
    });
});
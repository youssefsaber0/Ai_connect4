class Board {
  constructor(wrapper) {
    this.container = wrapper
    this.turn = "red"
    this.state = "7777777"

    this.__initBoard()
    Object.preventExtensions()
  }

  __initBoard() {
    for (let col = 0; col < 7; col++) {
      $(this.container).append(`
        <div class="col" col="${col}"></div>
      `);
      for (let row = 0; row < 6; row++) {
        $(this.container).find("[col=" + col + "]").append(`
          <div class="slot"></div>
        `)
      }
    }
  }

  $(selector) {
    return $(this.container).find(selector)
  }

  drop(col) {
    if(this.state[col] == 0)
      throw new ColumnOverflow;

    // Drop piece
    let slot = this.$(`[col=${col}] .slot:nth-child(${parseInt(this.state[col])})`)
    $(slot).addClass(`${this.turn}-slot`)

    // Update state
    this.state = this.state.replaceAt(col, this.state[col] - 1)
    this.turn = this.turn == "red" ? "yellow" : "red"

  }
}

class ColumnOverflow extends Error {
  constructor(){
    super("Column is filled")
  }
}
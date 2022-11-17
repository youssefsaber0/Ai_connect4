class Board {
  constructor(wrapper) {
    this.container = wrapper
    this.turn = "red"
    this.state = "6666666"

    this.__initBoard()
    Object.preventExtensions()
  }

  __initBoard() {
    this.__turn(this.turn)
    $("#score1").html(0)
    $("#score2").html(0)

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

  __turn(turn) {
    $("#turn").html(turn + "'s turn").css("color", `var(--${turn})`)
  }

  drop(col) {
    if(this.state[col] == 0)
      throw new ColumnOverflow;

    // Drop piece
    let slot = this.$(`[col=${col}] .slot:nth-child(${parseInt(this.state[col])})`)
    console.log(`[col=${col}] .slot:nth-child(${parseInt(this.state[col])})`)
    $(slot).addClass(`${this.turn}-slot`)

    // Update state
    this.state = this.state.replaceAt(col, this.state[col] - 1)
    this.turn = this.turn == "red" ? "yellow" : "red"
    this.__turn(this.turn)
  }

  reset() {
    this.$(".yellow-slot").removeClass("yellow-slot")
    this.$(".red-slot").removeClass("red-slot")
    this.state = "6666666"
    this.turn = "red"

    this.__turn("red")
    $("#score1").html(0)
    $("#score2").html(0)
  }
}

class ColumnOverflow extends Error {
  constructor(){
    super("Column is filled")
  }
}
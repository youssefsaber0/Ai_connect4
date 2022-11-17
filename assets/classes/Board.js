class Board {
  PLAYER = "red"
  BOT = "yellow"

  constructor(wrapper) {
    this.container = wrapper
    this.turn = this.PLAYER
    this.state = "6666666"

    this.__initBoard()
    Object.preventExtensions()
  }

  __initBoard() {
    this.showTurn()
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

  showTurn(turn=null) {
    if(turn)
      this.turn = turn   

    $("#turn").html(this.turn + "'s turn").css("color", `var(--${this.turn})`)
  }

  __toggleTurn() {
    this.showTurn(this.turn == this.PLAYER ? this.BOT : this.PLAYER)
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
    this.__toggleTurn()
  }
}

class ColumnOverflow extends Error {
  constructor(){
    super("Column is filled")
    this.name = "ColumnOverflow"
  }
}
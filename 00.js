const TamTamBotAPI = require('node-tamtam-bot-api');

// Replace the ACCESS_TOKEN with your own token obtained from the TamTam developer console.
const ACCESS_TOKEN = "XzgPQGjHPzXu-ptpZuBSpZaFZnbdiHxfoQb4Q5WcXAM";

const bot = new TamTamBotAPI(ACCESS_TOKEN);

// List of words that are not allowed in the chat
const BANNED_WORDS = ["badword1", "badword2", "badword3"];

// Handle new messages
bot.on('message_created', async (update) => {
  const message = update.message;
  const chatId = message.recipient.chat_id;

  // Check if the message contains banned words and remove them
  for (const word of BANNED_WORDS) {
    if (message.body.text.toLowerCase().includes(word)) {
      await bot.deleteMessage(chatId, message.body.mid);
      await bot.sendMessage(chatId, { text: "🚫 الرسائل المحتويه على الكلمات المحظورة لا يمكن نشرها." });
      break;
    }
  }
});

// Handle chat member updates
bot.on('chat_member', async (update) => {
  const chatMemberUpdate = update.chat_member_update;
  const chatId = chatMemberUpdate.chat_id;
  
  if (chatMemberUpdate.action.type === "join") {
    const newMember = chatMemberUpdate.action.member.user_id;
    await bot.sendMessage(chatId, { text: `مرحبا بك في المجموعة، ${newMember}!` });
  } else if (chatMemberUpdate.action.type === "leave") {
    const leftMember = chatMemberUpdate.action.member.user_id;
    await bot.sendMessage(chatId, { text: `وداعا، ${leftMember}!` });
  }
});

// Start the bot
bot.startPolling();

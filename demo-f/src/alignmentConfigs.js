import { reactive } from "vue";
// exports some reactive configuration objects
// these contain defaults for generating embeddings for different embedding types
// currently only word2vec is supported
export const selectedAlignment = reactive({
  topKType:'Top % Tokens',
  alignmentType: "global"
});
export const cls = reactive({
	  modelTypes: ["nn", "svm_auto", "svm_features"]
});

export const topKOptions = reactive({
	'Top K Tokens':{
		type:'topk',
		value:1000,
	},
	'Top % Tokens':{
		type:'percent',
		value:100,
	}
})
export const availableAlignments = reactive({
	"global":{
	},
	"noise-aware":{
		"is_soft":true,
	},
	"s4":{
		"cls_model": "nn",
		"iters": 100,
		"n_targets": 10,
		"n_negatives": 10,
		"fast": true,
		"rate": 0,
		"t": 0.5,
		"t_overlap": 0.5
	}
});

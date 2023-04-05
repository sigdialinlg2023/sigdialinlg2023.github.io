**Evaluating NLG systems: a brief introduction**

*Emiel van Miltenburg*



This year INLG will feature an award for the paper with the best evaluation. The purpose of this award is to provide an incentive for NLG researchers to pay more attention to the way they assess the output of their systems. This blog provides a short introduction to evaluation in NLG, explaining key terms and distinctions.

**How can I evaluate my system?**

It is hard to say in general how you should evaluate your NLG system. Much depends on the kind of system that you are developing, and the context in which it is being used. A first step is to get used to commonly used terminology in the field, so that you know what possibilities are out there.

*Intrinsic evaluation* refers to the assessment of system output in isolation. For example, grammaticality is a property that you can assess using intrinsic evaluation. You could use either *human evaluation* (e.g. grammaticality judgments) or *automatic metrics* (e.g. a precision grammar or a grammar checker) to determine whether the output of an NLG system is grammatical. (For an overview of different properties that you could evaluate, see [Belz et al. , 2020](https://aclanthology.org/2020.inlg-1.24/).) Finally, you could carry out an *error analysis* to determine where the system still falls short.

*Extrinsic evaluation* refers to the impact that a system may have on downstream processes. If you have a newly developed NLG system, you could for example see whether employees become more efficient or more productive after the system has been deployed.

Sometimes people also use the term “extrinsic evaluation” to assess the impact of a specific module in an NLG pipeline. An *intrinsic* evaluation of an NLG pipeline module would just look at the quality of its output, rather than the final text that is produced by the full pipeline. You could carry out an *extrinsic* evaluation by determining the extent to which the final output improves when you replace an existing module (e.g. for rule-based referring expression generation) with a newly developed module. 

If you are developing multiple new modules, you could carry out *ablation tests* (systematically leaving out or replacing different modules) to see how much each new module contributes to the system’s overall performance.

For a more in-depth overview, see e.g. [Celikyilmaz et al. (2020)](https://arxiv.org/abs/2006.14799) or [Sai et al. (2022)](https://dl.acm.org/doi/abs/10.1145/3485766).

**Human versus automatic evaluation**

Human evaluation is generally seen as the gold standard in NLG research, because in the end it is essential that human readers appreciate the output of your system. Having that said, there is great value in reliable automatic metrics, since they are cheaper and not as labor-intensive. Reliability is the keyword here: no matter how you measure different properties of the generated text, we have to be able to trust the conclusions that you draw from your observations.

**What are current best practices in the field?**

It is always risky to talk about best practices, because evaluation is so context-dependent. As the saying goes: “a foolish consistency is the hobgoblin of little minds” (Emerson 1841). For some projects, it may be better to deviate from existing standards. Having said that, here are ten steps you may find useful in planning your evaluation. Some of these steps raise fundamental questions about your research project, so it is important to start thinking about evaluation at the start of your project, and to not consider evaluation as an afterthought. Moreover, good evaluations take time, which means you need to schedule enough time to carry out a reliable evaluation.

1. *Determine the target audience.* Who are you developing your NLG system for? Ideally you will evaluate the performance of your system with a group of participants that matches the demographic properties of your target audience. Even if you don’t carry out a human evaluation, it is still important to understand the application context because of the next point.

2. *Get to know user needs*. If you have an applied NLG project, you should ideally start from an understanding of the stakeholders’ needs. That means talking to the people who will use your system, getting to know what they want to do with your system and what properties are important for them. Then you can develop an evaluation protocol that is in line with user needs.

3. *Identify relevant work.* Search for relevant literature, identifying models you want to compare to and metrics that are commonly used. Determine if those metrics make sense given your project. Consider reproducing relevant results, to be able to carry out any comparisons yourself.

4. *Determine your goals and expectations*. Based on the earlier steps, formulate a relevant research question. Think about possible outcomes of your project, which outcome is more likely, and why you expect this to be the case. Also consider how different outcomes of your evaluation should be interpreted. Try to be as precise as possible. Does it make sense to form hypotheses about your experiments, and to motivate them on the basis of earlier literature? This helps with theory building in NLG. 

5. - *Identify key independent variables.* There are many factors that could influence the characteristics of the output text. Different sets of inputs lead to different kinds of outputs, and different system properties affect the way the output text looks. Your job is to identify the main variables of interest.
   - *Determine key dependent variables*. There are many different properties of NLG output that you could assess, for example: grammaticality, fluency, completeness, naturalness, appropriateness, and the list goes on. You don’t have space to cover them all (although you could provide an additional extensive evaluation in the appendix), and some properties are probably more relevant than others for the purpose of your project. Clearly define the constructs of interest before you start thinking about how to operationalise those constructs. Use those definitions to critically assess the metrics you are planning to use.

6. *Check the validity of your set-up.* Having identified all relevant variables, you can operationalise the different dependent variable through different kinds of metrics. Here it is important to ensure the validity of your metrics. In other words: do your metrics measure what they are supposed to measure? One way to ensure the validity of a metric is to study the correlation between that metric and a trusted reference, such as human judgments. (Ehud Reiter [investigated](https://aclanthology.org/J18-3002/) this in detail for the BLEU metric.) Alternatively you could think of theoretical arguments to motivate why your metric provides a good approximation of the variable of interest.

7. *Select a sensible subset for evaluation.* If you cannot evaluate all the output of your model (and possibly the models that you are comparing your work to), think about the way you are sampling the outputs-to-be-evaluated. The sampling procedure heavily impacts the validity of your evaluation and the generalisability of your results.

8. *Get IRB approval (if appropriate for your study).* When you know what the evaluation will look like, you can apply for approval with your local institutional review board (IRB, also known as ‘ethics committee’) to determine that your study follows current ethics guidelines. If you do this at the onset of your project, you are less likely to run into any procedural delays. With a research proposal for the IRB in hand, you may also decide to turn the proposal into a full preregistration of your study (see [Van Miltenburg et al., 2021](https://aclanthology.org/2021.naacl-main.51/)).

9. *Keep a log.* Carry out your study and note any deviations from your original plans, including the reasons why you changed your mind. These insights are essential to provide the rationale behind your study design. If you do not write this information down, you will forget it. For example, you could create a private GitHub repository to hold all your code, data, and notes. (Once your project is done, you can publish the repository alongside your paper. There are also [services](https://anonymous.4open.science) to create a link to an anonymised version of your repository, that you can include in your submitted paper.) Or you could manage your project through the [Open Science Foundation](https://osf.io) (OSF). 

10. *Be explicit about your materials and methods.* Report all relevant information about how you carried out your evaluation, so that others could reproduce your work using only your paper. If you carry out a human evaluation, the [Human Evaluation DataSheet](https://aclanthology.org/2022.humeval-1.6/) provides an overview of important details to record.

11. *Describe all relevant results*. If you are reporting overall scores, consider providing a table with disaggregated results for different subsets of the input data. Next to overview tables, you may also want to create insightful visualisations of the results. (Though choose wisely; don’t just duplicate your results in another modality.) Go beyond the “higher is better” narrative and explain what the results mean for your system and the NLG literature in general. Be open about the limitations of your evaluation and the challenges that still lie ahead. 



**Bonus tip**: *archive all data associated with your study.* This includes including all outputs for the validation and test sets, crowdsourcing templates, aggregated and [non-aggregated](https://pdai.info) human ratings, outputs of statistical analysis software). Small files might be included in your GitHub repository, but otherwise data can be hosted through other services, e.g. OSF, [Zenodo](https://zenodo.org), [Figshare](https://figshare.com), organisational repository or national science hosting provider. It is possible that not all data can be made available at submission time (though it is often possible to share data anonymously), but at least try to be as exhaustive as possible for your camera-ready version.

For more in-depth reading, here are some useful references:

- [Van Miltenburg et al. (2021)](https://aclanthology.org/2021.inlg-1.14/) provide guidelines for error analysis.
- [Van der Lee et al. (2021)](https://www.sciencedirect.com/science/article/pii/S088523082030084X) provide recommendations for human evaluation studies.
- [Gehrmann et al. (2022)](https://arxiv.org/abs/2202.06935) provide general recommendations regarding both human and automatic evaluations.
- [Ehud Reiter’s blog](https://ehudreiter.com/blog-index/) has more recommendations for evaluating NLG systems.

If you have any questions, the community discord channel is a great place to ask questions. Contact Dave Howcroft ([D.Howcroft@napier.ac.uk](mailto:D.Howcroft@napier.ac.uk)) for an invitation.

*Thanks to Simone Balloccu, Ondřej Dušek, Dave Howcroft, Maria Keet, Ember Manning, Maja Popović, Craig Thomson, and Sina Zarrieß for feedback on an earlier draft of this blog post.*
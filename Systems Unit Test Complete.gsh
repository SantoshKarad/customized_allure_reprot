pipeline {
    agent any
    environment {
        toolPath = 'D:/HodgesE/tools/'
    }
    parameters {
        string(name: 'revisionId', defaultValue: '')
        booleanParam(name: 'rebuild', defaultValue: true, description: 'Recompile all projects')
        string(name: 'configBranch', defaultValue: 'main', description: 'Repository branch containing the configuration')
    }
    options {
        timeout(time: 3, unit: "HOURS")
    }
    stages {
        stage('Checkout input sources') {
            steps {
                script {
                    currentBuild.displayName = "Revision ${params.revisionId}"
                }
                cleanWs()
                dir('systemsdata') {
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/${configBranch}"]],
                        userRemoteConfigs: [[
                            url: 'https://gitlab.dematic.com/GlobalControls/systemsdata.git',
                            credentialsId: '0db853c0-00ea-454d-a3e2-9660e396dc4b',
                        ]]
                    ])
                }
                bat "xcopy systemsdata\\conveyors\\att_configuration\\*.xml . /s /y"
                script {
                    if (rebuild.toBoolean()) {
                        bat "xcopy \"D:\\MultiUser\\Systems\\${params.revisionId}\\\" \"D:\\MultiUser\\Systems\\${params.revisionId}_1\\\" /s /y"
                        bat "xcopy \"D:\\MultiUser\\Systems\\${params.revisionId}\\\" \"D:\\MultiUser\\Systems\\${params.revisionId}_2\\\" /s /y"
                        bat "xcopy \"D:\\MultiUser\\Systems\\${params.revisionId}\\\" \"D:\\MultiUser\\Systems\\${params.revisionId}_3\\\" /s /y"
                        bat "xcopy \"D:\\MultiUser\\Systems\\${params.revisionId}\\\" \"D:\\MultiUser\\Systems\\${params.revisionId}_4\\\" /s /y"
                    }
                }
            }
        }
        stage ('Build') {
            parallel {
                stage ('Test Build 1') {
                    when { expression { return rebuild.toBoolean() }}
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            dir('systemsdata/conveyors/composer') {
                                bat "${env.toolPath}BuildComposer/BuildComposer.exe \"D:\\MultiUser\\Systems\\${params.revisionId}_1\\Systems\\Systems.ap17\" ComposerCfg_incremental_100_1b.xml"
                                junit skipPublishingChecks: true, testResults: "compile-1-report.xml"
                            }
                        }
                    }
                }
                stage ('Test Build 2') {
                    when { expression { return rebuild.toBoolean() }}
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            dir('systemsdata/conveyors/composer') {
                                bat "${env.toolPath}BuildComposer/BuildComposer.exe \"D:\\MultiUser\\Systems\\${params.revisionId}_2\\Systems\\Systems.ap17\" ComposerCfg_incremental_100_2b.xml"
                                junit skipPublishingChecks: true, testResults: "compile-2-report.xml"
                            }
                        }
                    }
                }
                stage ('Test Build 3') {
                    when { expression { return rebuild.toBoolean() }}
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            dir('systemsdata/conveyors/composer') {
                                bat "${env.toolPath}BuildComposer/BuildComposer.exe \"D:\\MultiUser\\Systems\\${params.revisionId}_3\\Systems\\Systems.ap17\" ComposerCfg_incremental_100_3b.xml"
                                junit skipPublishingChecks: true, testResults: "compile-3-report.xml"
                            }
                        }
                    }
                }
                stage ('Test Build 4') {
                    when { expression { return rebuild.toBoolean() }}
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                            dir('systemsdata/conveyors/composer') {
                                bat "${env.toolPath}BuildComposer/BuildComposer.exe \"D:\\MultiUser\\Systems\\${params.revisionId}_4\\Systems\\Systems.ap17\" ComposerCfg_incremental_100_4b.xml"
                                junit skipPublishingChecks: true, testResults: "compile-4-report.xml"
                            }
                        }
                    }
                }
            }
        }
        stage('Export') {
            when { expression { return rebuild.toBoolean() }}
            steps {
                dir('systemsdata/conveyors/composer') {
                    // Export and map
                    bat "xcopy \"temp1\\\" \"D:\\MultiUser\\export\\${params.revisionId}\\\" /s /y /r"
                    bat "xcopy \"temp2\\\" \"D:\\MultiUser\\export\\${params.revisionId}\\\" /s /y /r"
                    bat "xcopy \"temp3\\\" \"D:\\MultiUser\\export\\${params.revisionId}\\\" /s /y /r"
                    bat "xcopy \"temp4\\\" \"D:\\MultiUser\\export\\${params.revisionId}\\\" /s /y /r"
                    bat "xcopy \"*report.xml\" \"D:\\MultiUser\\export\\${params.revisionId}\\*\" /y /r"
                }
            }
        }
        stage('Load stage 1 simulation instance') {
            steps {
                bat "plcsim_load_setup.py"
                bat "py -m dematic.tools.scripts.plcsim_load --revision ${revisionId} --autodir ./systemsdata/tia_automation/automation --project \"D:\\MultiUser\\Systems\\${revisionId}_1\\Systems\\Systems.ap17\" --composer_cfg ./systemsdata/conveyors/composer/ComposerCfg_100.xml --artefact_path ./systemsdata/tia_automation/automation/temp/artefacts"
                bat "plcsim_unit_setup.py"
            }
        }
        stage('Unit test stage 1') {
            options {
                timeout(time: 10, unit: "MINUTES")
            }
            steps {
                bat "${env.toolPath}AutoTestTool/ATTConsoleProj.exe exec_cfg_test_inc_1b.xml"
                junit skipPublishingChecks: true, testResults: "inc-1-report.xml"
            }
        }
        stage('Load stage 2 simulation instance') {
            steps {
                bat "py -m dematic.tools.scripts.plcsim_load --revision ${revisionId} --autodir ./systemsdata/tia_automation/automation --project \"D:\\MultiUser\\Systems\\${revisionId}_2\\Systems\\Systems.ap17\" --composer_cfg ./systemsdata/conveyors/composer/ComposerCfg_100.xml --artefact_path ./systemsdata/tia_automation/automation/temp/artefacts"
                bat "plcsim_unit_setup.py"
            }
        }
        stage('Unit test stage 2') {
            options {
                timeout(time: 10, unit: "MINUTES")
            }
            steps {
                bat "${env.toolPath}AutoTestTool/ATTConsoleProj.exe exec_cfg_test_inc_2b.xml"
                junit skipPublishingChecks: true, testResults: "inc-2-report.xml"
            }
        }
        stage('Load stage 3 simulation instance') {
            steps {
                bat "py -m dematic.tools.scripts.plcsim_load --revision ${revisionId} --autodir ./systemsdata/tia_automation/automation --project \"D:\\MultiUser\\Systems\\${revisionId}_3\\Systems\\Systems.ap17\" --composer_cfg ./systemsdata/conveyors/composer/ComposerCfg_100.xml --artefact_path ./systemsdata/tia_automation/automation/temp/artefacts"
                bat "plcsim_unit_setup.py"
            }
        }
        stage('Unit test stage 3') {
            options {
                timeout(time: 10, unit: "MINUTES")
            }
            steps {
                bat "${env.toolPath}AutoTestTool/ATTConsoleProj.exe exec_cfg_test_inc_3b.xml"
                junit skipPublishingChecks: true, testResults: "inc-3-report.xml"
            }
        }
        stage('Load stage 4 simulation instance') {
            steps {
                bat "py -m dematic.tools.scripts.plcsim_load --revision ${revisionId} --autodir ./systemsdata/tia_automation/automation --project \"D:\\MultiUser\\Systems\\${revisionId}_4\\Systems\\Systems.ap17\" --composer_cfg ./systemsdata/conveyors/composer/ComposerCfg_100.xml --artefact_path ./systemsdata/tia_automation/automation/temp/artefacts"
                bat "plcsim_unit_setup.py"
            }
        }
        stage('Unit test stage 4') {
            options {
                timeout(time: 10, unit: "MINUTES")
            }
            steps {
                bat "${env.toolPath}AutoTestTool/ATTConsoleProj.exe exec_cfg_test_inc_4b.xml"
                junit skipPublishingChecks: true, testResults: "inc-4-report.xml"
            }
        }
        stage('Teardown'){
            steps {
                bat "@echo off & plcsim_unit_teardown.py"
            }
        }
    }
    post {
        success {
            build wait: false, propagate: false, job: 'WIP/Dependency Based Systems Unit Test', parameters: [string(name: 'revisionId', value: "${revisionId}"), booleanParam(name: 'regenerateGraph', value: true)]
        }
        unstable{
            build wait: false, propagate: false, job: 'WIP/Dependency Based Systems Unit Test', parameters: [string(name: 'revisionId', value: "${revisionId}"), booleanParam(name: 'regenerateGraph', value: true)]
        }
        failure {
            steps {
                bat '@echo Complete failure'
            }
        }
    }
}
